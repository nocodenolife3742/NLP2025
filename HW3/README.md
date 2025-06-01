# NLP HW3 NER 

```
111590002 鄭重雨 - NER 程式撰寫 (50%)
111590004 張意昌 - 模型修改測試、文件撰寫 (50%)
```

## Request

除 `requirements.txt` 內文件所需 `module` ， 請確認以下事情

- 是否有 `Nvidia` 顯示卡
- 電腦是否有安裝 `CUDA` ， `CMD` 使用 `nvcc --version` 可查看
- `torch` 是否為 `CUDA` 版本

若上述有一點沒達成，則會使用 `CPU` 進行訓練，可能會使 `Demo` 過久  
以下有簡易安裝方法

## Cuda Download

先輸入
```
nvidia-smi
```
後查看 `CUDA` 版本 (第一行)  
之後去安裝對應的 `CUDA` 版本  
[CUDA Download](https://developer.nvidia.com/cuda-toolkit-archive)

`nvcc --version` 若有資訊，就代表安裝成功

之後再去安裝 `Pytorch` (需依照對應 `CUDA` 版本)  

[Pytorch Download](https://pytorch.org/get-started/previous-versions/)

## Usage

由上而下執行即可  
訓練時間依照顯卡 (或是 `CPU` ) 效能不同  
`RTX 2060` 大約跑 `10` ~ `20` 分鐘 ( `VRAM 6G` )

## Question & Solve

```
在本次作業中，我們要實作一個 `NER` 辨識器
目的在於透過給定句子進行文字分析，並預測詞性
```

```
我們的方法如下
1. 下載資料集
2. 資料處理
3. 將標籤轉成數字
4. 切分訓練、驗證、測試
5. 準備資料集 
6. Tokenizer 將句子斷詞並與標籤對齊
7. Fine Tune 模型
8. 測試結果 - 4 分數
9. 測試結果 - 透過給定句子進行預測
```

```
我們使用了 `hugging face` 上面的 `Transformer` 進行此次訓練
一開始是使用 `distilbert/distilbert-base-uncased` 進行訓練
但後來發現效果不佳，主要原因是 `Precision`、`Recall`、`F1 Score` 大約 `0.76` 上下
所以經過找尋其他的 `Transformer` ，認為 `FacebookAI/roberta-base` 
是我們這次的折衷方案，效果良好且訓練時長不會太久
`Precision`、`Recall`、`F1 Score` 大約 `0.83` 上下
且也有一定機會可以分辨出 `.` 屬於句號還是縮寫的意義
```

```
以下是可以改進的方向

1. 參考 `NER` 相關模型，進行測試
2. 增加更多資料集
3. 嘗試不同參數
4. 使用 `CRF` 後處理機制
```

## Result

依照最後模型得到結果如下

```
Evaluation results:
Precision: 0.8243
Recall: 0.8394
F1 Score: 0.8318
Accuracy: 0.9637
```

```
Sentence: The capital of France is Paris.
Entity:  The capital of, Label: O, Score: 0.9996
Entity:  France, Label: B-LOC, Score: 0.9971
Entity:  is, Label: O, Score: 0.9998
Entity:  Paris., Label: B-LOC, Score: 0.7564

Sentence: Apple Inc. is a technology company based in Cupertino.
Entity:  Apple, Label: B-ORG, Score: 0.9980
Entity:  Inc., Label: I-ORG, Score: 0.9954
Entity:  is a technology company based in, Label: O, Score: 0.9998
Entity:  Cupertino., Label: B-LOC, Score: 0.8757

Sentence: Barack Obama was the 44th President of the United States.
Entity:  Barack, Label: B-PER, Score: 0.9935
Entity:  Obama, Label: I-PER, Score: 0.9976
Entity:  was the 44th President of the, Label: O, Score: 0.9990
Entity:  United, Label: B-LOC, Score: 0.9662
Entity:  States, Label: I-LOC, Score: 0.9812
Entity: ., Label: O, Score: 0.5609
```