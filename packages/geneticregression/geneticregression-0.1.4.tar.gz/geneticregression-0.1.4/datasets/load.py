import os
import pandas as pd


def load_dataset_from_dir(dir_path):

    # Raise error if not a valid directory path
    if not os.path.isdir(dir_path):
        raise ValueError(f'{dir_path} is not a valid directory path')

    # Get file names from directory
    data_files, config_file = get_dir_fnames(dir_path)

    # Interpret the configuration file
    cfg_prms = interpret_cfg(f'{dir_path}/{config_file}')

    # Load in the files
    files = {}
    for ftype in ('train', 'validation', 'test'):
        # Extract name from cfg params
        fname = cfg_prms.get(ftype)
        # Skip if no name provided
        if fname is None:
            continue
        # Load in from pandas
        if fname[-3:] == 'csv':
            df = pd.read_csv(f'{dir_path}/{fname}')
        elif fname[-7:] == 'feather' or fname[-3:] == 'fea':
            df = pd.read_feather(f'{dir_path}/{fname}')
        elif fname[-7:] == 'parquet':
            df = pd.read_parquet(f'{dir_path}/{fname}')
        else:
            raise Exception

        og_cols = list(df.columns)
        columns = [df.columns[c] for c in cfg_prms['feat_cols']]
        columns.append(df.columns[cfg_prms['lbl_col']])
        onehots = [df.columns[c] for c in cfg_prms.get('onehot',())]

        df = df[columns]

        df = pd.get_dummies(df, columns=onehots)

        files[ftype] = df

    return files


'''
def load(inp, **kargs):
    df = pd.read_csv(inp, delimiter=kargs.get('sep',','))

    feat_cols = [df.columns[i] for i in kargs.get('feat_cols',\
                                                range(0,len(df.columns)-1))]
    lbl_col = df.columns[kargs.get('lbl_col',-1)]

    return df[feat_cols].to_numpy(), df[lbl_col].to_numpy(), feat_cols, lbl_col
'''

def get_dir_fnames(dir_path):
    # Stores csv files and config files
    data_files, config_file = [], None

    # Iterate through directory provided
    for fname in os.listdir(dir_path):

        # Get file extension
        file_ext = fname.split('.')[-1]

        if file_ext.lower() in ('csv','feather','parquet'):
            data_files.append(fname)
        elif file_ext == 'cfg': # Save config file
            # Raise an error if already have a configuration file
            if config_file is not None:
                raise Exception \
                    (f'Multiple cfg files in {dir_path}:\n{fname},{config_file}')
            # Store the config file
            config_file = fname

    return data_files, config_file

def interpret_cfg(cfg_file):

    def interpret_col_ranges(p_val):
        f_cols, temp_lst = [], p_val.split(',')
        for val in temp_lst:
            if '-' in val:
                # Split to get lower / upper bound
                bounds = val.split('-')
                # Raise error if split into more than min/max
                if len(bounds) > 2:
                    raise ValueError\
                        ('Cannot have multiple \'-\' per range of cols')
                # Add all values in that range
                f_cols.extend(list(range(int(bounds[0]),int(bounds[1]))))
            else:
                f_cols.append(int(val))
        return f_cols

    # Read the file
    with open(cfg_file, 'r') as F:
        lines = F.readlines()

    # Stores parameters
    cfg_prms = dict.fromkeys(('train','validation','test','feat_cols',\
                                        'lbl_col','delimeter','onehot'))

    # Iterate through and gather important info
    for line in lines:

        # Split line, make sure only one : character
        line_split = line.split(':')
        if len(line_split) > 2:
            raise Exception('Cannot include additional \':\' characters')
        p_name, p_val = line_split

        # Verify not already defined
        if cfg_prms[p_name] is not None:
            raise Exception(f'{p_name} is listed twice in {cfg_file}')

        # Remove spaces
        p_val = p_val.replace(' ','').replace('\t','').replace('\n','')

        # If training, validation, or test file
        if p_name in ('train', 'validation', 'test'):
            cfg_prms[p_name] = p_val

        elif p_name == 'feat_cols':

            cfg_prms[p_name] = interpret_col_ranges(p_val)

            # Verify label is not in features
            if cfg_prms['lbl_col'] is not None and cfg_prms['lbl_col'] in f_cols:
                raise Exception('lbl_col cannot be in feat_cols')

        elif p_name == 'onehot':
            cfg_prms[p_name] = interpret_col_ranges(p_val)

        elif p_name == 'lbl_col':
            # Get value
            cfg_prms['lbl_col'] = int(p_val)

            if cfg_prms['feat_cols'] is not None and \
                                cfg_prms['lbl_col'] in cfg_prms['feat_cols']:
                raise Exception('lbl_col cannot be in feat_cols')

        else:
            cfg_prms[p_name] = p_val

    print(cfg_prms)
    return cfg_prms
