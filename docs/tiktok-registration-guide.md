# TikTok Developers 登録ガイド (FieldRise)

このドキュメントは、FieldRiseのブランド拡大のためにTikTok APIを利用するための登録情報をまとめたものです。

## 1. 登録に必要な基本情報

TikTok Developers Console (https://developers.tiktok.com/) で以下の情報を入力してください。

| 項目 | 入力内容 |
| :--- | :--- |
| **App Name** | FieldRise Brand Manager |
| **Description** | AI-driven management system for 'Cafe series' global BGM brand. |
| **Website URL** | `https://hatsuhiko8215.github.io/FieldRise/index.html` |
| **Privacy Policy URL** | `https://hatsuhiko8215.github.io/FieldRise/privacy.html` |
| **Terms of Service URL** | `https://hatsuhiko8215.github.io/FieldRise/terms.html` |

## 2. Login Kit / OAuth 設定 (必要な場合)

もしOAuth連携を行う場合は、以下のリダイレクトURIを設定してください。

- **Redirect URI:** `https://hatsuhiko8215.github.io/FieldRise/auth/callback.html`
  *(※現在はプレースホルダーですが、審査には必要です)*

## 3. 審査に向けたヒント

- **アプリアイコン:** FieldRiseのロゴ（またはシンプルな青と黒のアイコン）をアップロードしてください。
- **利用目的:** 「自社ブランド 'Cafe series' の投稿分析およびパフォーマンス追跡のため」と説明してください。

## 4. APIキー取得後の流れ

1. **Client Key** と **Client Secret** を取得してください。
2. それらを安全な方法（GitHub Secretsなど）で管理します。
3. 桃花 (Manus) に「APIキーを取得した」と伝えていただければ、実装を開始します。
