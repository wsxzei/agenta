export default function HomePage() {
    return (
        // min-h-screen: 最小高度为屏幕高度; flex: 使用 Flexbox 布局 https://juejin.cn/post/7004622232378966046
        // items-center 垂直居中; justify-center 居中；bg-gray-50: 背景色灰色-50
        <div className="min-h-screen flex items-center justify-center bg-gray-50">
            <div className="text-center">
                {/*
                    text-4xl 字体大小为特大; font-bold: 字体加粗; mb-4 下边距 1rem
                */}
                <h1 className="text-4xl font-bold text-gray-900 mb-4">
                    欢迎使用 Agenta 前端学习项目
                </h1>
                <p className="text-lg text-gray-600">
                    这是一个从零开始的学习项目
                </p>
            </div>
        </div>
    )
}

