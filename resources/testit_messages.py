import testit


def add_flow_success_message(
        flow_name,
        request_code=None,
        request=None,
        checks=None,
        **details,
):
    lines = [
        "✅ Флоу успешно завершён",
        f"Сценарий: {flow_name}",
        f"RequestCode: {request_code}",
        "",
    ]
    if request:
        lines.extend(["Состояние запроса:"])
        lines.extend([ f"Status: {request['Status']}"])
        lines.extend([f"InboundProblem: {request['InboundProblem']}"])
        lines.extend([f"ResolveReason: {request['ResolveReason']}"])

    if checks:
        lines.extend(["", "Проверки:"])
        lines.extend(f"— {check}" for check in checks)

    if details:
        lines.extend(["", "Дополнительные данные:"])
        lines.extend(f"{key}: {value}" for key, value in details.items())

    testit.addMessage("\n".join(lines))
