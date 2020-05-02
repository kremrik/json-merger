def merge(raw: dict, master: dict) -> dict:
    if not master:
        return master

    output = {}
    raw_keys = raw.keys()
    master_keys = master.keys()
    

    for m_key, m_type in master.items():
        if m_key in raw.keys():
            if isinstance(raw[m_key], m_type):
                msg = f"{m_key} is a valid key"
                output[m_key] = raw[m_key]
            else:
                r_val = raw[m_key]
                r_type = type(r_val)
                msg = f"'{r_val}' was cast to {m_type}"
                output[m_key] = m_type(r_val)
        else:
            msg = f"Missing key '{m_key}'"
            output[m_key] = None
        print(msg)

    for r_key, r_val in raw.items():
        if r_key not in master.keys():
            msg = f"Key '{r_key}' was not in master schema"
            output[r_key] = r_val
        print(msg)

    return output
