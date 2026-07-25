from config import Config


def main():

    cfg = Config()

    print("=" * 50)
    print("LiveTranslate")
    print("=" * 50)

    print("Whisper :", cfg.get("whisper_model"))
    print("Translator :", cfg.get("translator"))
    print("Target :", cfg.get("target_language"))

    print("\nStage 1 初始化完成")


if __name__ == "__main__":
    main()