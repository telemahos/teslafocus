import logging

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def calculate_battery_capacity(model, trim, wltp_range):
    if not wltp_range or not isinstance(wltp_range, str):
        logger.warning(f"Invalid WLTP range value: {wltp_range}")
        return None

    try:
        range_value = int(''.join(filter(str.isdigit, wltp_range)))
    except ValueError:
        logger.warning(f"Could not extract numeric value from WLTP range: {wltp_range}")
        return None
    
    # PAWD, LRAWD, MYRWD
    # MODEL 3
    if model == "m3" and trim == "M3RWD":
        if range_value == 409:
            return 53.1
        elif range_value == 448: 
            return 55.0 #LFP
        elif range_value == 491:
            return 60.0

    if model == "m3" and trim == "LRAWD":
        if range_value == 560:
            return 78.8
        elif range_value == 580:
            return 75.0
        elif range_value == 614:
            return 82.0
        elif range_value == 602:
            return 78.1

    if model == "m3" and trim == "PAWD":
        if range_value == 530:
            return 78.8
        elif range_value == 567: 
            return 82.0 
        elif range_value == 547:
            return 78.1
        
    # PAWD, LRAWD, MYRWD
    # MODEL Y
    if model == "my" and trim == "MYRWD":
        if range_value == 455:
            return 60.0 #LFP

    if model == "my" and trim == "LRAWD":
        if range_value == 507:
            return 75.0
        elif range_value == 533:
            return 78.1
        elif range_value == 565:
            return 78.1

    if model == "my" and trim == "PAWD":
        if range_value == 514:
            return 78.1

    return None  # Return None if no matching condition is found