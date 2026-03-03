# doubao-video-gen

## description
调用豆包 Seedance 2 API 生成视频

## usage
生成指定描述的视频文件

## args
- prompt: 视频描述文本（必填）
- output: 输出文件路径（可选，默认./output.mp4）
- width: 视频宽度（可选，默认1080）
- height: 视频高度（可选，默认1920）

## examples
生成一只猫跳舞的视频:
$ doubao-video-gen --prompt "一只橘猫在草地上跳舞" --output ./cat.mp4

## notes
- 需要设置环境变量 DOUBAO_API_KEY
- 视频生成需要一定时间，请耐心等待
