def read_config_file(filepath):
    # Bug: Exception handling issue - catching BaseException (too broad) and silencing it completely without logs
    try:
        with open(filepath, 'r') as f:
            return f.read()
    except BaseException:
        # Silently fails, caller doesn't know what error occurred (file not found vs permission vs disk fail)
        return None
