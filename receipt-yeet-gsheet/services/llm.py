from groq import Groq
import json
import os


def parse_receipt_text(ocr_text):
    client = Groq(api_key=os.getenv('GROQ_API_KEY'))

    prompt_path = os.path.join(os.path.dirname(__file__), "prompt.txt")
    with open(prompt_path, "r") as f:
        prompt = f.read()
    prompt = prompt.replace("<<RECEIPT_TEXT>>", ocr_text)

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"},
    )

    content = response.choices[0].message.content
    try:
        return json.loads(content)
    except Exception:
        # Fallback to empty object if the model returns non-JSON
        return {}


def main(argv=None):
    from dotenv import load_dotenv
    load_dotenv()
    
    from ocr import ocr_image
    # ocr_text = ocr_image("/Users/mits-mac-001/Code/receipt-yeet-gsheet/test2.jpg")
    ocr_text = """maruetsu
petit
プチ
西新宿六丁目店 03-3343-6560
領収証
登録番号 T8013301012770
2025年12月15日 (月) 07:56
店:09390 レジ No:6503
415 昆布おにぎり
158※
415 鮭づくしおにぎり
198※
小計
(8%外税対象額
2点
¥356
¥356)
8%外税額
合計
PayPay
¥28
¥384
¥384
※印は軽減税率適用商品です。
全店でWAON POINTが
たまります! つかえます!
PayPay 売上票
(お客様控え用)
取引内容
端末識別番号
GW 取引通番
ご利用額
売上
6304620539053
176575299356596
¥384
レシートNo:3946
貴: 45088025塩"""
    parsed_data = parse_receipt_text(ocr_text)
    print(json.dumps(parsed_data, ensure_ascii=False))


if __name__ == "__main__":
    main()
    #todo add details about to how to parse the receipts from different shits. 
    # like screenshot from paypay
    # maruetsu receipts usually has the code for each item that's printed before the item name and then proceeds with value of the item. 