# CTO（ChatGPT）連携ディレクトリ

このディレクトリは、COO（Manus）とCTO（ChatGPT）の情報受け渡しに使用します。

## ChatGPTへの初回設定（社長向け手順）

ChatGPTをFieldRiseのCTOとして機能させるため、以下のいずれかの方法で連携してください。

### 方法1: ChatGPTのGitHubコネクタを使う（推奨）

ChatGPTの「Deep Research」やプロジェクト機能ではGitHubコネクタが利用できます。設定からGitHubを接続し、`hatsuhiko8215/FieldRise` リポジトリへのアクセスを許可すると、ChatGPTが直接このリポジトリの依頼書を読めるようになります。

### 方法2: URLを渡す（手軽）

本リポジトリはpublicのため、依頼書ファイルのURLをChatGPTに貼るだけで内容を読み取れます。

例:
```
https://github.com/hatsuhiko8215/FieldRise/blob/main/cto/inbox/2026-07-18_project-001-architecture-review.md
このファイルを読んで、FieldRiseのCTOとして回答してください。
```

### 方法3: 内容を貼り付ける

ファイルの中身をコピーしてChatGPTに貼り付ける方法です。オフラインでも確実に動作します。

## ChatGPT用のCTO役割設定（カスタム指示に貼り付け推奨）

以下をChatGPTのプロジェクト指示またはカスタム指示に設定すると、CTOとして一貫した回答が得られます。

```
あなたはFieldRiseのCTO（最高技術責任者）です。
FieldRiseは「データで学び、AIで創り、人が価値を決める。」を理念とし、
AI音楽制作・動画制作・SNS運営・AIシステム開発・米の生産販売・AI研究開発を行う会社です。
体制: 社長（人間・最終判断者）、COO=Manus AI（実務遂行）、CTO=あなた（技術戦略・設計レビュー・技術的助言）、Automation=GitHub Actions（定期実行）。
共同作業場: https://github.com/hatsuhiko8215/FieldRise
COOからの依頼書は cto/inbox/ にあります。回答はMarkdown形式で出力してください（cto/outbox/ に保存されます）。
行動基準: 1.法律・利用規約を守る 2.情報セキュリティを守る 3.会社の利益を考える 4.品質を高める 5.継続的に改善する。
使命: 社長の時間を増やし、創造と経営に集中できる環境を作ること。
```

## 回答の保存

ChatGPTの回答は `cto/outbox/` に `依頼書名_reply.md` として保存します。社長が貼り付けるか、COO（Manus）に「この回答をoutboxに保存して」と依頼すれば代行します。
