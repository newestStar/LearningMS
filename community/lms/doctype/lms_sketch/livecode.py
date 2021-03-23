"""Utilities to work with livecode service.
"""
import websocket
import json
import drawSvg as draw

def livecode_to_svg(livecode_ws_url, code, *, timeout=1):
    """Renders the code as svg.
    """
    print("livecode_to_svg")
    ws = websocket.WebSocket()
    ws.settimeout(timeout)
    ws.connect(livecode_ws_url)

    msg = {
        "msgtype": "exec",
        "runtime": "python-canvas",
        "code": code
    }
    ws.send(json.dumps(msg))

    messages = _read_messages(ws)
    commands = [m['cmd'] for m in messages if m['msgtype'] == 'draw']
    img = draw_image(commands)
    return img.asSvg()

def _read_messages(ws):
    messages = []
    try:
        while True:
            msg = ws.recv()
            if not msg:
                break
            messages.append(json.loads(msg))
    except websocket.WebSocketTimeoutException:
        pass
    return messages

def draw_image(commands):
    img = draw.Drawing(300, 300, origin=(0, -300), fill='none', stroke='black')
    for c in commands:
        if c['function'] == 'circle':
            img.append(draw.Circle(cx=c['x'], cy=c['y'], r=c['d']/2))
        elif c['function'] == 'line':
            img.append(draw.Line(sx=c['x1'], sy=c['y1'], ex=c['x2'], ey=c['y2']))
        elif c['function'] == 'rect':
            img.append(draw.Rectangle(x=c['x'], y=c['y'], width=c['w'], height=c['h']))
    return img
