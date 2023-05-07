#!/bin/bash

# test.pyを実行して結果を変数に代入する
result=$(python3 update_profiles/login_google.py )

if [ $result = true ]; then
  echo "処理が正常に完了しました"
else
  echo "処理に失敗しました"
  git add .
  git commit -m "Automated commit message"
  git push origin main
fi