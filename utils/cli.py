import argparse


def parse_commandline_args():
    return create_parser().parse_args()


def create_parser():
    parser = argparse.ArgumentParser(description='PyTorch Mean-Teacher Training')
    parser.add_argument('--input_rdx_file', type=str, default='data/rdx/root-ontology.owl',
                        help='the file in rdx format which needs to be converted to yaml format for eidos')