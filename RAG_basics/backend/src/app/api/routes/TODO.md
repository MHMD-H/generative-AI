# Route TODOs

الجداول دي محتاجة قرار duplicate check قبل ما نعمل لها POST:

- `guardians`: مفيش unique field في الجدول. الهينت: هل رقم التليفون يكفي؟ ولا ممكن ولي أمرين يشتركوا في نفس الرقم؟
- `communications`: غالبا كل رسالة event جديد، فممكن ميبقاش لها duplicate check أصلا.
- `announcements`: محتاج قرار: هل التكرار يكون بنفس `title` و `audience`؟ ولا الإعلان ممكن يتكرر؟
- `reports`: محتاج قرار: هل التكرار يكون بنفس `title`, `report_type`, وكيان مرتبط؟
- `documents`: عندك `content_hash` unique لكنه nullable. الهينت: خلي ingestion pipeline يولد hash دايما قبل إنشاء document.
- `chat_sessions`: غالبا session جديدة كل مرة، فمفيش unique طبيعي.
- `chat_messages`: غالبا الرسائل تتكرر عادي داخل المحادثة، فمفيش unique طبيعي.
