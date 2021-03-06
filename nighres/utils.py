import os
import warnings
import urllib
from global_settings import TOPOLOGY_LUT_DIR, ATLAS_DIR, DEFAULT_ATLAS


def download_from_url(url, filename, overwrite_file=False):

    dirname = os.path.dirname(filename)
    if not os.path.isdir(dirname):
        os.makedirs(dirname)

    if os.path.isfile(filename) and overwrite_file is False:
        print("\nThe file {0} exists and overwrite_file was set to False -- "
              "not downloading.").format(filename)
    else:
        print("\nDownloading to {0}").format(filename)
        urllib.urlretrieve(url, filename)


def _output_dir_4saving(output_dir=None, rootfile=None):
    if output_dir is None:
        if rootfile is None:
            # if nothing is specified, use current working dir
            output_dir = os.getcwd()
        else:
            # if rootfile is specified, use it's directory
            output_dir = os.path.dirname(rootfile)

    # create directory recursively if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # make sure path ends on seperator
    if not(output_dir[-1] == os.path.sep):
        output_dir += os.path.sep

    # check if there is write access to the directory
    if not os.access(output_dir, os.W_OK | os.X_OK):
        raise ValueError("Cannot write to {0}, please specify a different "
                         "output_dir. (Note that if you don't set output_dir "
                         "explicitly, it will be set to the directory of the "
                         "input file, if applicable, or to the current "
                         "working directory otherwise)").format(output_dir)

    print("\nOutputs will be saved to {0}").format(output_dir)
    return output_dir


def _fname_4saving(rootfile=None, suffix=None,
                   base_name=None, extension=None):
    # if both base_name and extension are given, jump right to inserting suffix
    if (base_name is None or extension is None):
        # else, if a rootfile is given, find base_name and extension
        if isinstance(rootfile, basestring):
            # avoid empty strings
            if len(rootfile) <= 1:
                raise ValueError("When trying to determine the file name for "
                                 "saving from the input {0}, the input file "
                                 "name seems empty. Check if your inputs "
                                 "exist, or try to specify the base_name "
                                 "parameter for saving.").format(rootfile)
            split_root = os.path.basename(rootfile).split('.')
            # if there was only one dot in the filename, it is good to go
            if len(split_root) == 2:
                base = split_root[0]
                ext = split_root[1]
            else:
                # pop file extension
                ext = split_root.pop(-1)
                # file extension could have two parts if compressed
                if ext == 'gz':
                    ext = split_root.pop(-1)+'.gz'
                # now that the extension has been popped out of the list
                # what's left is the basename, put back together
                base = split_root.pop(0)
                while split_root:
                    base += '.'+split_root.pop(0)
            # use rootfile parts only for what's missing
            if not base_name:
                base_name = base
            if not extension:
                extension = ext
        # if the input is not a filename but a data object both base_name
        # and extension should be given, raise warning and make surrogate
        else:
            if base_name is None:
                base_name = 'output'
            if extension is None:
                extension = 'nii.gz'

            warnings.warn(("If passing a data object as input, you should "
                           "specify a base_name AND extension for saving. "
                           "Saving to %s.%s (plus suffixes) for now")
                          % (base_name, extension))

    # insert suffix if given
    if suffix is not None:
        base_name += '_' + suffix

    # putting it all together
    fname = base_name + '.' + extension

    return fname


def _check_topology_lut_dir(topology_lut_dir):

    if topology_lut_dir is None:
        topology_lut_dir = TOPOLOGY_LUT_DIR
    else:
        # check if dir exists
        if not os.path.isdir(topology_lut_dir):
            raise ValueError('The topology_lut_dir you have specified ({0}) '
                             'does not exist'.format(topology_lut_dir))
    # make sure there is a  trailing slash
    topology_lut_dir = os.path.join(topology_lut_dir, '')

    return topology_lut_dir


def _check_atlas_file(atlas_file):

    if atlas_file is None:
        atlas_file = DEFAULT_ATLAS
    else:
        # check if file exists, if not try search atlas in default atlas dir
        if not os.path.isfile(atlas_file):
            if not os.path.isfile(os.path.join(ATLAS_DIR, atlas_file)):
                raise ValueError('The atlas_file you have specified ({0}) '
                                 'does not exist'.format(atlas_file))
            else:
                atlas_file = os.path.join(ATLAS_DIR, atlas_file)

    return atlas_file
