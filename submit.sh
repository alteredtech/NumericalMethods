#!/bin/bash
echo 'This will stage all and commit to master branch'
read -p 'Enter your commit:' commit
git stage -A && git commit -m "$commit" && git push