# api

## post 

url: https://api.dialogue.moe

Content-Type:application/json

| key        | value   | default | example    |
| :-----     | :-----  | :-----  | :-----     |
| text       | string  |         | 我很好奇    |
| bangumi_id | string  |         | 27364      |
| duplicate  | boolean | false   | true       |

## response

| key                             | value   | example  |
| :-----                          | :-----  | :-----   |
| total                           | string  | 4773     |
| time_cost                       | string  | 23       |
| dialogues                       | array   |          |
| dialogues.dialogues_id          | string  | 258034_23_292  |
| dialogues.subject_id            | string  | 27364    |
| dialogues.subject_name          | string  | 冰菓      |
| dialogues.ep                    | string  | 22       |
| dialogues.score                 | float   | 22.804   |
| dialogues.sub_title             | string  |          |
| dialogues.file_name             | string  |          |
| dialogues.text_before           | string  | 我很好奇…   |
| dialogues.time_current          | string  | 00:14:12   |
| dialogues.text_current          | string  | 我很好奇…   |
| dialogues.text_current_highlight| string  | &lt;em>我&lt;/em>&lt;em>很&lt;/em>&lt;em>好奇&lt;/em>…  |
| dialogues.text_after            | string  | 要是我现在能从正面看到涂着口红  微微俯首的千反田   |
| dialogues.sort_values           | array   |         |
