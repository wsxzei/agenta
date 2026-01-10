import type {Config} from "tailwindcss"

const config: Config = {
    content: [
        "./src/**/*.{js,ts,jsx,tsx}",  // 扫描的文件
    ],
    theme: {
        extend: {},  // 扩展主题
    },
    plugins: [],    // 插件
    corePlugins: {
        preflight: false,  // 关闭 Preflight（避免与 Ant Design 冲突）
    },
}

export default config

