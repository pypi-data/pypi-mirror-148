"""
Tool to collect and show Tensorboard for multiple models
Call with model ids or an application id to select data to show in Tensorboard
"""
import argparse
import json
import os
import re
import tempfile
import time

from brevettiai.platform import PlatformAPI
from tensorboard import program
from tqdm import tqdm

from pandas import json_normalize
import tensorflow as tf
from tensorboard.plugins.hparams import api as hp

type_mapper = {
    type(None): lambda x: "None",
    list: str,
}


def dict_to_hparam(obj, logdir, trial_id=None):
    normalized = json_normalize(obj).iloc[0].to_dict()

    safe = {k: type_mapper.get(type(v), lambda x: x)(v) for k, v in normalized.items()}
    with tf.summary.create_file_writer(logdir).as_default():
        hp.hparams(safe, trial_id=trial_id)


def _get_models(model_ids, web: PlatformAPI = None):
    """Retrieve models from web ids sorted by creation"""
    models = web.get_model()
    models = sorted((m for m in models if m.id in model_ids), key=lambda m: m.created, reverse=True)
    return models


def application_tensorboard(application, web: PlatformAPI = None):
    """Start tensorboard with models on application"""
    web = web or PlatformAPI()
    if isinstance(application, str):
        application = web.get_application(application)
    models = _get_models(model_ids=application.model_ids, web=web)
    model_tensorboard(models, web=web)


def model_tensorboard(models: list, web: PlatformAPI = None):
    """Start tensorboard with specified models"""
    web = web or PlatformAPI()

    # If model is string use it as id to get model
    models = [web.get_model(model) if isinstance(model, str) else model for model in models]

    with tempfile.TemporaryDirectory() as tmpdir:

        tb = program.TensorBoard()
        tb.configure(argv=[None, '--logdir', tmpdir])
        url = tb.launch()
        print(f"Tensorflow listening on {url}")

        for model in tqdm(models):

            logname = re.sub(r'[\\/*?:"<>|]', "", f"{model.name} {model.created}").rstrip()
            logdir = os.path.join(tmpdir, logname)

            artifacts = web.get_artifacts(model, prefix="events.out.tfevents")
            for artifact in artifacts:
                if artifact.size < 100e6:
                    dst = os.path.join(logdir, "events.out.tfevents" + artifact.name)
                    web.download_url(artifact.link, dst)
                else:
                    print(f"Skipping: {artifact.link}")

            artifacts = web.get_artifacts(model, prefix="tensorboard/")
            for artifact in artifacts:
                if artifact.size < 100e6:
                    dst = os.path.join(logdir, "events.out.tfevents" + artifact.name)
                    web.download_url(artifact.link, dst)
                else:
                    print(f"Skipping: {artifact.link}")

            output_files = web.get_artifacts(model, prefix="output.json")
            if output_files:
                output = json.loads(web.download_url(output_files[0].link).content)
                try:
                    dict_to_hparam(output.get("job", output.get("config"))["settings"], logdir, trial_id=logname)

                    if not output["output"]:
                        output["output"]["no_metrics"] = 1

                    with tf.summary.create_file_writer(logdir).as_default():
                        for k, v in output["output"].items():
                            tf.summary.scalar(k, v, step=-1)
                except Exception:
                    print("Warning: error", model.name)

        if not os.listdir(tmpdir):
            print("No tensorboards found")
        else:
            while True:
                time.sleep(1000)


def main(target):
    """ Run Tensorboard collector"""
    web = PlatformAPI()
    if len(target) == 1:
        try:
            web.get_model(target[0])
        except PermissionError:
            application = web.get_application(target[0])
            if application:
                application_tensorboard(application, web=web)
                quit()

    model_tensorboard(target, web=web)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('target', nargs='+', help="Application id or space separated model ids")
    args = parser.parse_args()

    main(args.target)
