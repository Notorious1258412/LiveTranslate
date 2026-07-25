import pyaudiowpatch as pyaudio


def get_audio_devices():

    p=pyaudio.PyAudio()
    devices=[]

    for i in range(p.get_device_count()):

        dev=p.get_device_info_by_index(i)

        if dev.get("isLoopbackDevice") and dev.get("maxInputChannels",0)>0:

            devices.append({
                "index":i,
                "name":dev["name"],
                "rate":int(dev["defaultSampleRate"]),
                "channels":dev["maxInputChannels"]
            })

    p.terminate()

    return devices



def get_default_loopback():

    p=pyaudio.PyAudio()

    try:

        default=p.get_default_output_device_info()

        default_name=default["name"]

        print("Windows 預設音效:")
        print(default_name)


        print("")
        print("可用 Loopback:")


        for i in range(p.get_device_count()):

            dev=p.get_device_info_by_index(i)

            if dev.get("isLoopbackDevice"):

                print(
                    i,
                    dev["name"]
                )


        print("")


        for i in range(p.get_device_count()):

            dev=p.get_device_info_by_index(i)

            if not dev.get("isLoopbackDevice"):
                continue


            loop_name=dev["name"]


            clean_loop=loop_name.replace(
                " [Loopback]",
                ""
            )


            if (
                default_name in loop_name
                or
                clean_loop in default_name
                or
                default_name.replace(" ","") in clean_loop.replace(" ","")
            ):

                print("使用 Loopback:")
                print(loop_name)

                print(
                    "index:",
                    i
                )

                print(
                    "rate:",
                    dev["defaultSampleRate"]
                )

                print(
                    "channels:",
                    dev["maxInputChannels"]
                )


                return p,i,{
                    "name":loop_name,
                    "defaultSampleRate":int(
                        dev["defaultSampleRate"]
                    ),
                    "maxInputChannels":dev["maxInputChannels"]
                }


        raise Exception(
            "找不到預設音效 Loopback: "+default_name
        )


    except Exception:

        p.terminate()
        raise



def get_audio_device(name=None):

    p=pyaudio.PyAudio()

    for i in range(p.get_device_count()):

        dev=p.get_device_info_by_index(i)

        if dev.get("isLoopbackDevice") and dev.get("maxInputChannels",0)>0:

            if name is None or dev["name"]==name:

                print("使用裝置:")
                print(dev["name"])

                return p,i,{
                    "name":dev["name"],
                    "defaultSampleRate":int(
                        dev["defaultSampleRate"]
                    ),
                    "maxInputChannels":dev["maxInputChannels"]
                }


    p.terminate()

    raise Exception(
        "找不到指定音訊裝置: "+str(name)
    )