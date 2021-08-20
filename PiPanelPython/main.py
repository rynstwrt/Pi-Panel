from flask import Flask, request
import json
import programs


app = Flask(__name__)


buttons = {
    "pride flag": programs.program_pride_flag,
    "camera": programs.program_camera,
    "edge detection": programs.program_edge_detection,
    "equalizer": programs.program_equalizer,
    "trippy": programs.program_trippy,
    "monitor": programs.program_monitor,
    "modified sine": programs.program_modified_sine,
    "waveform": programs.program_waveform,
    "spectrum analyzer": programs.program_spectrum_analyzer
}


@app.route("/getbuttons", methods=["GET"])
def get_buttons():
    programs = list(buttons.keys())
    return json.dumps({"buttons": programs})


@app.route("/setprogram", methods=["POST"])
def set_program():
    data = request.data
    program_name = json.loads(data)["program"].lower()
    buttons[program_name]()
    return program_name


if __name__ == "__main__":
    app.run(port=5000)