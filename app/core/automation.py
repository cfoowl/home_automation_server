def check_condition(condition: dict, value) -> bool:
    match condition["type"]:
        case "bool":
            return int(condition["value"]) == value
        case "number":
            return evaluate_numeral_condition(value, condition["operator"], int(condition["value"]))

def evaluate_numeral_condition(value, operator: str, threshold):
    match operator:
        case ">":
            return value > threshold
        case ">=":
            return value >= threshold
        case "<":
            return value < threshold
        case "<=":
            return value <= threshold
        case "=":
            return value == threshold
        case "!=":
            return value != threshold
