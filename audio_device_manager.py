import pyaudiowpatch as pyaudio


def get_loopback_devices():

    p=pyaudio.PyAudio()

    devices=[]

    for i in range(
        p.get_device_count()
    ):

        dev=p.get_device_info_by_index(i)

        if dev.get(
            "isLoopbackDevice"
        ):

            devices.append(
                dev["name"]
            )

    p.terminate()

    return devices