#!/usr/bin/env python3

import cv2
import json
import logging
import numpy as np
import os
import random
from typing import List

import detectron2
from detectron2.utils.logger import setup_logger
from detectron2.data.datasets import register_coco_instances
from detectron2.utils.logger import setup_logger
from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.utils.visualizer import Visualizer
from detectron2.data import MetadataCatalog, DatasetCatalog, datasets
from detectron2.structures import BoxMode
from detectron2.engine import DefaultTrainer
from detectron2.structures import BoxMode
# from google.colab.patches import cv2_imshow

from bioblu.detectron import detectron
from bioblu.ds_manage import ds_annotations
from bioblu.ds_manage import ds_convert

if __name__ == "__main__":
    loglevel = logging.INFO
    logformat = "[%(levelname)s]\t%(funcName)15s: %(message)s"
    logging.basicConfig(level=loglevel, format=logformat)
    # logging.disable()

    # Detectron2 logger
    setup_logger()

    # DS setup
    materials_dict: dict = {0: "trash"}
    yolo_ds_root_dir: str = "/opt/nfs/shared/scratch/bioblu/datasets/dataset_05_mini_gnejna"
    # bioblu_dir: str = "/opt/nfs/shared/scratch/bioblu"
    detectron_ds_target_dir = os.path.join(yolo_ds_root_dir + "_detectron")

    ds_convert.cvt_yolo_to_detectron(yolo_ds_root_dir, materials_dict=materials_dict)

    img_dir_train: str = os.path.join(detectron_ds_target_dir, "train")
    img_dir_valid: str = os.path.join(detectron_ds_target_dir, "val")

    # Extract image dict lists from jsons
    fpath_json_train = os.path.join(detectron_ds_target_dir, "annotations", "instances_detectron_train.json")
    fpath_json_valid = os.path.join(detectron_ds_target_dir, "annotations", "instances_detectron_val.json")
    fpath_json_test = os.path.join(detectron_ds_target_dir, "annotations", "instances_detectron_test.json")

    logging.info(f"Training images: {img_dir_train}")
    logging.info(f"Validation images: {img_dir_valid}")
    logging.info(f"Training json: {fpath_json_train}")
    logging.info(f"Validate json: {fpath_json_valid}")
    logging.info(f"Testing json: {fpath_json_test}")

    train_imgs: List[dict] = detectron.create_detectron_img_dict_list(fpath_json_train)
    valid_imgs: List[dict] = detectron.create_detectron_img_dict_list(fpath_json_valid)
    test_imgs: List[dict] = detectron.create_detectron_img_dict_list(fpath_json_test)
    logging.info("Img. dict lists extracted.")

    classes = materials_dict.values()
    logging.info("Classes registered.")

    # Registering dataset
    # DatasetCatalog.register("trash_train", lambda: detectron.create_detectron_img_dict_list(fpath_json_train))
    # DatasetCatalog.register("trash_valid", lambda: detectron.create_detectron_img_dict_list(fpath_json_valid))
    # # DatasetCatalog.register("trash_test", lambda: detectron.create_detectron_img_dict_list(fpath_json_test))
    datasets.register_coco_instances("trash_train", {}, fpath_json_train, img_dir_train) # added in 4865
    datasets.register_coco_instances("trash_valid", {}, fpath_json_valid, img_dir_valid) # added in 4865
    logging.info("Dataset registered.")

    # Registering metadata
    MetadataCatalog.get("trash_train").set(thing_classes=list(classes))
    MetadataCatalog.get("trash_valid").set(thing_classes=list(classes))
    # MetadataCatalog.get("trash_test").set(thing_classes=classes)
    # metadata_train = MetadataCatalog.get("trash_train") # updated in 4865
    # metadata_valid = MetadataCatalog.get("trash_valid") # updated in 4865
    logging.info("Metadata registered.")

    logging.info("Creating cfg...")
    cfg = get_cfg()
    cfg.DATASETS.TRAIN = ("trash_train",)
    cfg.DATASETS.TEST = ("trash_valid",)  # ("valid",)
    logging.info("Added TRAIN and TEST cfg.DATASET attributes.")

    cfg.merge_from_file(model_zoo.get_config_file("COCO-Detection/faster_rcnn_R_50_C4_1x.yaml"))
    logging.debug("Merged from model zoo.")

    cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-Detection/faster_rcnn_R_50_C4_1x.yaml")  # Let training initialize from model zoo
    logging.info("Loaded model weights checkpoint from model zoo.")

    logging.info("Assigning worker numders, batch ims, lr and max iterations....")
    cfg.DATALOADER.NUM_WORKERS = 2
    cfg.SOLVER.IMS_PER_BATCH = 2
    cfg.SOLVER.BASE_LR = 0.00025  # pick a good LR
    cfg.SOLVER.MAX_ITER = 1200    # 300 iterations seems good enough for the tutorial dataset; you will need to train longer for a practical dataset
    cfg.SOLVER.STEPS = []        # do not decay learning rate
    cfg.MODEL.ROI_HEADS.BATCH_SIZE_PER_IMAGE = 128   # faster, and good enough for this toy dataset (default: 512)
    # ToDo: Perhaps add the proposal files:
    # cfg.DATASETS.PROPOSAL_FILES_TRAIN =
    cfg.MODEL.ROI_HEADS.NUM_CLASSES = 1  # only has one class (ballon). (see https://detectron2.readthedocs.io/tutorials/datasets.html#update-the-config-for-new-datasets)     # NOTE: this config means the number of classes, but a few popular unofficial tutorials incorrect uses num_classes+1 here.
    cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5  # set threshold for this model

    os.makedirs(cfg.OUTPUT_DIR, exist_ok=True)
    logging.debug("Created output dir.")

    # Save the accessible dataset version:
    dataset_test_out = DatasetCatalog.get("trash_train")
    with open(cfg.OUTPUT_DIR + "/dataset_cfg.json", "w") as f:
        json.dump(dataset_test_out, f, indent=4)


    trainer = DefaultTrainer(cfg)
    logging.debug("Done setting up trainer.")
    # trainer.resume_or_load(resume=False)
    # logging.debug("Starting training.")
    # trainer.train()

    # json_fpath = "/media/findux/DATA/Documents/Malta_II/datasets/dataset_04_gnejna_with_duplicates_COCO/annotations/gnejna_train.json"
    # ds_annotations.save_readable_json(json_fpath, "/home/findux/Desktop/gnejna_train.json")
    # img_dict_list = detectron.create_detectron_img_dict_list(json_fpath)
    # ds_annotations.save_to_json(img_dict_list, "/home/findux/Desktop/img_dict_list.json")