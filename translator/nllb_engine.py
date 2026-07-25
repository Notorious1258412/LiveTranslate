import os
import torch
from transformers import AutoModelForSeq2SeqLM,AutoTokenizer

class NLLBTranslator:

    def __init__(self, model_name="facebook/nllb-200-distilled-1.3B"):

        safe_name=model_name.replace(
            "/",
            "--"
        )

        local_path=os.path.join(
            "MODEL",
            "translate",
            "models--"+safe_name
        )

        print(
            "檢查翻譯模型:",
            os.path.abspath(local_path)
        )

        if os.path.exists(
            local_path
        ):
            print(
                "載入本機翻譯模型:",
                local_path
            )
            model_path=local_path
        else:
            print(
                "載入下載翻譯模型:",
                model_name
            )
            model_path=model_name


        self.tokenizer=AutoTokenizer.from_pretrained(
            model_path
        )

        self.model=AutoModelForSeq2SeqLM.from_pretrained(
            model_path,
            torch_dtype="auto"
        )

        self.src_lang="eng_Latn"
        self.target_lang="zho_Hant"

        print("NLLB模型載入完成")

    def translate(self,text):

        if not text:
            return ""


        self.tokenizer.src_lang=self.src_lang


        inputs=self.tokenizer(
            text,
            return_tensors="pt"
        )


        target_id=self.tokenizer.convert_tokens_to_ids(
            self.target_lang
        )


        translated=self.model.generate(
            **inputs,
            forced_bos_token_id=target_id,
            max_length=512
        )


        return self.tokenizer.batch_decode(
            translated,
            skip_special_tokens=True
        )[0]

