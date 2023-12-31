import os
import numpy as np

from dataset.customDataset import Custom_Dataset
from dataset.cifar10 import subsetCIFAR10


def init_datasets(args, transform_train, transform_test):
    if args.dataset == "imagenet":
        # Data loading code
        root, txt_train, txt_val, txt_test, pathReplaceDict = get_imagenet_root_split(args.data, args.customSplit)

        train_datasets = Custom_Dataset(root=root, txt=txt_train, transform=transform_train, pathReplace=pathReplaceDict)
        val_datasets = Custom_Dataset(root=root, txt=txt_val, transform=transform_test, pathReplace=pathReplaceDict)
        test_datasets = Custom_Dataset(root=root, txt=txt_test, transform=transform_test, pathReplace=pathReplaceDict)
    elif args.dataset == "imagenet100":
        # Data loading code
        root, txt_train, txt_val, txt_test, pathReplaceDict = get_imagenet100_root_split(args.data, args.customSplit)

        train_datasets = Custom_Dataset(root=root, txt=txt_train, transform=transform_train, pathReplace=pathReplaceDict)
        val_datasets = Custom_Dataset(root=root, txt=txt_val, transform=transform_test, pathReplace=pathReplaceDict)
        test_datasets = Custom_Dataset(root=root, txt=txt_test, transform=transform_test, pathReplace=pathReplaceDict)
    elif args.dataset == "cifar10":
        # the data distribution
        root, train_idx, val_idx = get_cifar10_data_split(args.data, args.customSplit)

        train_idx = list(np.load(train_idx))
        val_idx = list(np.load(val_idx))
        train_datasets = subsetCIFAR10(root=root, sublist=train_idx, transform=transform_train, download=True)
        val_datasets = subsetCIFAR10(root=root, sublist=val_idx, transform=transform_test, download=True)
        test_datasets = subsetCIFAR10(root=root, sublist=[], train=False, transform=transform_test, download=True)
    elif args.dataset == 'Pet37':
        root, txt_train, txt_val, txt_test = get_pet37_data_split(args.data, args.customSplit)

        train_datasets = Custom_Dataset(root=root, txt=txt_train, transform=transform_train)
        val_datasets = Custom_Dataset(root=root, txt=txt_val, transform=transform_test)
        test_datasets = Custom_Dataset(root=root, txt=txt_test, transform=transform_test)
    elif args.dataset == 'food101':
        root, txt_train, txt_val, txt_test = get_food101_data_split(args.data, args.customSplit)

        train_datasets = Custom_Dataset(root=root, txt=txt_train, transform=transform_train)
        val_datasets = Custom_Dataset(root=root, txt=txt_val, transform=transform_test)
        test_datasets = Custom_Dataset(root=root, txt=txt_test, transform=transform_test)
    else:
        raise ValueError("No such dataset: {}".format(args.dataset))

    return train_datasets, val_datasets, test_datasets


def get_imagenet_root_path(root):

    pathReplaceDict = {}
    if os.path.isdir(root):
        pass
    elif os.path.isdir("/mnt/models/imagenet_new"):
        root = "/mnt/models/imagenet_new"
        pathReplaceDict = {"train/": "train_new/"}
    else:
        assert False, "No dir for imagenet"

    return root, pathReplaceDict


def get_imagenet_root_split(root, customSplit, domesticAnimalSplit=False):
    root, pathReplaceDict = get_imagenet_root_path(root)

    txt_train = "split/imagenet/imagenet_train.txt"
    txt_val = "split/imagenet/imagenet_val.txt"
    txt_test = "split/imagenet/imagenet_val.txt"

    if domesticAnimalSplit:
        txt_train = "split/imagenet/imagenet_domestic_train.txt"
        txt_val = "split/imagenet/imagenet_domestic_val.txt"
        txt_test = "split/imagenet/imagenet_domestic_test.txt"

    if customSplit != '':
        txt_train = "split/imagenet/{}.txt".format(customSplit)

    return root, txt_train, txt_val, txt_test, pathReplaceDict


def get_imagenet100_root_split(root, customSplit):
    root, pathReplaceDict = get_imagenet_root_path(root)

    txt_train = "split/imagenet/ImageNet_100_train.txt"
    txt_val = "split/imagenet/ImageNet_100_val.txt"
    txt_test = "split/imagenet/ImageNet_100_test.txt"

    if customSplit != '':
        txt_train = "split/imagenet/{}.txt".format(customSplit)

    return root, txt_train, txt_val, txt_test, pathReplaceDict


def get_cifar10_data_split(root, customSplit, ssl=False):
    # if ssl is True, use both train and val splits
    if os.path.isdir(root):
        root = root
    else:
        if os.path.isdir('../../data'):
            root = '../../data'
        elif os.path.isdir('/mnt/models/dataset/'):
            root = '/mnt/models/dataset/'
        else:
            assert False

    if ssl:
        assert customSplit == ''
        train_idx = "split/cifar10/trainValIdxList.npy"
        return root, train_idx, None

    train_idx = "split/cifar10/trainIdxList.npy"
    val_idx = "split/cifar10/valIdxList.npy"
    if customSplit != '':
        train_idx = "split/cifar10/{}.npy".format(customSplit)

    return root, train_idx, val_idx


def get_pet37_path(root):
    if os.path.isdir(root):
        root = root
    else:
        if os.path.isdir('/mnt/models/Pet37/images/'):
            root = '/mnt/models/Pet37/images/'
        else:
            assert False

    return root


def get_pet37_data_split(root, customSplit, ssl=False):
    root = get_pet37_path(root)

    txt_train = "split/Pet37/Pet37_train.txt"
    txt_val = "split/Pet37/Pet37_val.txt"
    txt_test = "split/Pet37/Pet37_test.txt"

    if customSplit != '':
        txt_train = "split/Pet37/{}.txt".format(customSplit)

    if ssl:
        assert customSplit == ''
        train_idx = "split/Pet37/Pet37_trainval.txt"
        return root, train_idx, None, None

    return root, txt_train, txt_val, txt_test


def get_food101_path(root):
    if os.path.isdir(root):
        root = root
    else:
        if os.path.isdir('/mnt/models/food-101/images/'):
            root = '/mnt/models/food-101/images/'
        else:
            assert False

    return root


def get_food101_data_split(root, customSplit, ssl=False):
    root = get_food101_path(root)

    txt_train = "split/food-101/food101_train.txt"
    txt_val = "split/food-101/food101_val.txt"
    txt_test = "split/food-101/food101_test.txt"

    if customSplit != '':
        txt_train = "split/food-101/{}.txt".format(customSplit)

    if ssl:
        assert customSplit == ''
        train_idx = "split/food-101/food101_trainval.txt"
        return root, train_idx, None, None

    return root, txt_train, txt_val, txt_test
