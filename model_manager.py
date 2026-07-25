import os

BASE_DIR=os.path.dirname(
    os.path.abspath(__file__)
)

MODEL_DIR=os.path.join(
    BASE_DIR,
    "MODEL"
)

def get_models(folder):
    path=os.path.join(
        MODEL_DIR,
        folder
    )

    print(
        "掃描:",
        path
    )

    if not os.path.exists(path):
        print("資料夾不存在")
        return []

    result=[]

    for name in os.listdir(path):

        full=os.path.join(
            path,
            name
        )

        print(
            "找到:",
            full
        )

        if os.path.isdir(full):
            result.append(name)

    print(
        "模型列表:",
        result
    )

    return sorted(result)

def get_whisper_models():

    models=get_models(
        "whisper"
    )

    result=[]

    for m in models:
        if "small.en" in m:
            result.append(
                "small.en"
            )
        elif "small" in m:
            result.append(
                "small"
            )

    return result

def get_translate_models():

    models=get_models(
        "translate"
    )

    result=[]

    for m in models:

        if "1.3B" in m:
            result.append(
                "facebook/nllb-200-distilled-1.3B"
            )

        elif "600M" in m:
            result.append(
                "facebook/nllb-200-distilled-600M"
            )

    return result