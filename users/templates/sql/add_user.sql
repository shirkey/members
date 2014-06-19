INSERT INTO
  user (guid, name, email, website, email_updates, longitude, latitude)
VALUES (
  "{{ guid }}",
  "{{ name }}",
  "{{ email }}" ,
  "{{ website }}",
  {{ email_updates }},
  {{ longitude }},
  {{ latitude }});
