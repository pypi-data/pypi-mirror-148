from hytk_model.hytk_detect import HytkDetect

hytk_detect = HytkDetect(384,384,10)
score,gray = hytk_detect.detect("https://upload-bbs.mihoyo.com/upload/2021/08/28/285326533/dafdc9a38a8fb08bd688ec73eac45d98_2730930178173092193.png","url")
print(score)