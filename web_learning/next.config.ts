import type {NextConfig} from "next"

const config: NextConfig = {
    reactStrictMode: true, // 启用 React 严格模式（开发时检测问题）
    pageExtensions: ["ts", "tsx", "js", "jsx"],
    eslint: {
        ignoreDuringBuilds: true, // 构建时忽略 ESLint 错误
    },
    typescript: {
        ignoreBuildErrors: true, // 构建时忽略 TS 错误
    },
}

export default config

