# import requests
# import json
# import re
# def parse_quiz_text(quiz_text):
#     quiz_text = quiz_text.replace('for accuracy):','for accuracy)')
#     quiz_text = re.sub(r'#.*\n', '', quiz_text)  # Remove quiz title
#     quiz_data = {}

#     # Split the input into questions and options
#     questions = re.findall(r'\*\*(\d+)\. (.*?)\*\*\n(.*?)\n\n', quiz_text, re.DOTALL)

#     for question in questions:
#         question_number = question[0]
#         question_text = question[1].strip()
#         options_text = question[2].strip().splitlines()

#         options = {}
#         for option in options_text:
#             match = re.match(r'([a-d])\.\s*(.*)', option)
#             if match:
#                 options[match.group(1)] = match.group(2).strip()

#         quiz_data[int(question_number)] = {
#             "text": question_text,
#             "options": options,
#             "answer": ""  # Placeholder for the answer
#         }

#     # Extract the answer key section
#     answer_key_section = re.search(r'Answer\sKey\s\([^\)]+\)\s*([\d\s\.\w]+)', quiz_text, re.DOTALL)
#     if answer_key_section:
#         answer_key_text = answer_key_section.group(1).strip()
#         answer_key_lines = answer_key_text.splitlines()

#         for line in answer_key_lines:
#             match = re.match(r'(\d+)\.\s*([a-d])', line.strip())
#             if match:
#                 question_number = int(match.group(1))
#                 answer = match.group(2)
#                 if question_number in quiz_data:
#                     quiz_data[question_number]["answer"] = answer

#     return quiz_data

# def get_questions(num_questions, topic, grade_level):


#     cookies = {
#         'locale': 'en-us',
#         'cookieyes-consent': 'consentid:ZzB1WmRKZ0k3TGxVdUhSb1drejR5dWREYml4VlNGTWc,consent:yes,action:no,necessary:yes,functional:yes,analytics:yes,performance:yes,advertisement:yes,other:yes,lastRenewedDate:1705991862000',
#         '_ga': 'GA1.1.934169142.1734513863',
#         'pi_opt_in1086533': 'true',
#         '_gcl_au': '1.1.783717375.1734513856.741403328.1734513872.1734513884',
#         'Authorization.0': 'base64-eyJhY2Nlc3NfdG9rZW4iOiJleUpoYkdjaU9pSklVekkxTmlJc0ltdHBaQ0k2SWxFM2JDOWlhV2hpWm1sNU9FSm5ha2dpTENKMGVYQWlPaUpLVjFRaWZRLmV5SmhZV3dpT2lKaFlXd3hJaXdpWVcxeUlqcGJleUp0WlhSb2IyUWlPaUp3WVhOemQyOXlaQ0lzSW5ScGJXVnpkR0Z0Y0NJNk1UY3pORFV4TXpnNE5IMWRMQ0poY0hCZmJXVjBZV1JoZEdFaU9uc2ljSEp2ZG1sa1pYSWlPaUpuYjI5bmJHVWlMQ0p3Y205MmFXUmxjbk1pT2xzaVoyOXZaMnhsSWwxOUxDSmhkV1FpT2lKaGRYUm9aVzUwYVdOaGRHVmtJaXdpWlcxaGFXd2lPaUp5WVdGbVlYUnpZVzFwTVRBeFFHZHRZV2xzTG1OdmJTSXNJbVY0Y0NJNk1UY3pORFl3TURJNE5Dd2lhV0YwSWpveE56TTBOVEV6T0RnMExDSnBjMTloYm05dWVXMXZkWE1pT21aaGJITmxMQ0pwYzNNaU9pSm9kSFJ3Y3pvdkwzUnVkWEI2ZUdacWNuVnJjM1ZzZG1aNVlXNXNMbk4xY0dGaVlYTmxMbU52TDJGMWRHZ3ZkakVpTENKd2FHOXVaU0k2SWlJc0luSnZiR1VpT2lKaGRYUm9aVzUwYVdOaGRHVmtJaXdpYzJWemMybHZibDlwWkNJNkltVTVPVGt3WlRNeExUZzNNakV0TkdabVpTMWlNMlprTFRnM1lUUTRNelZoTkRjd01TSXNJbk4xWWlJNklqTTJNemhoTTJFMUxXSTRPR1V0TkRCbFlTMDRNVGt5TFRBek5HUXlPVFJqT0RrNE15SXNJblZ6WlhKZmJXVjBZV1JoZEdFaU9uc2lZWFpoZEdGeVgzVnliQ0k2SW1oMGRIQnpPaTh2YkdnekxtZHZiMmRzWlhWelpYSmpiMjUwWlc1MExtTnZiUzloTDBGRFp6aHZZMHhaTUZCMlJFdEplamRzZFdsbVZtWnpkM1ZuUmpSYU0yVjNORUpIWDFvelpIUnNZV00xTVhGNWJVSmZNa3RmVW5NOWN6azJMV01pTENKamRYTjBiMjFmWTJ4aGFXMXpJanB1ZFd4c0xDSmxiV0ZwYkNJNkluSmhZV1poZEhOaGJXa3hNREZBWjIxaGFXd3VZMjl0SWl3aVpXMWhhV3hmZG1WeWFXWnBaV1FpT2lKMGNuVmxJaXdpWm5Wc2JGOXVZVzFsSWpvaWNtRmhabUYwSUhOaGJXa2lMQ0pwYzNNaU9pSm9kSFJ3Y3pvdkwyRmpZMjkxYm5SekxtZHZiMmRzWlM1amIyMGlMQ0p1WVcxbElqb2ljbUZoWm1GMElITmhiV2tpTENKd2FHOXVaVjkyWlhKcFptbGxaQ0k2SW1aaGJITmxJaXdpY0dsamRIVnlaU0k2SW1oMGRIQnpPaTh2YkdnekxtZHZiMmRzWlhWelpYSmpiMjUwWlc1MExtTnZiUzloTDBGRFp6aHZZMHhaTUZCMlJFdEplamRzZFdsbVZtWnpkM1ZuUmpSYU0yVjNORUpIWDFvelpIUnNZV00xTVhGNWJVSmZNa3RmVW5NOWN6azJMV01pTENKd2NtOTJhV1JsY2w5cFpDSTZJakV4TkRnMU16RTFNRGd5TVRVd01qVXpNRE0wTWlJc0luTjFZaUk2SWpFeE5EZzFNekUxTURneU1UVXdNalV6TURNME1pSjlmUS5aTmVJZ0JmZ2duMEw1QTRBRVRsR3c3a3lLdU5vOWR0ODh5MV9rQWRuMnJnIiwidG9rZW5fdHlwZSI6ImJlYXJlciIsImV4cGlyZXNfaW4iOjg2NDAwLCJleHBpcmVzX2F0IjoxNzM0NjAwMjg0LCJyZWZyZXNoX3Rva2VuIjoiQldLWG5WSVdwUWt5a0xJVGVVX0p3QSIsInVzZXIiOnsiaWQiOiIzNjM4YTNhNS1iODhlLTQwZWEtODE5Mi0wMzRkMjk0Yzg5ODMiLCJhdWQiOiJhdXRoZW50aWNhdGVkIiwicm9sZSI6ImF1dGhlbnRpY2F0ZWQiLCJlbWFpbCI6InJhYWZhdHNhbWkxMDFAZ21haWwuY29tIiwiZW1haWxfY29uZmlybWVkX2F0IjoiMjAyNC0wMS0wM1QxMzo0NzoxOC44ODUwNzJaIiwicGhvbmUiOiIiLCJjb25maXJtZWRfYXQiOiIyMDI0LTAxLTAzVDEzOjQ3OjE4Ljg4NTA3MloiLCJyZWNvdmVyeV9zZW50X2F0IjoiMjAyNC0wMy0xN1QxNzowNDoxMS4yMzU2NVoiLCJsYXN0X3NpZ25faW5fYXQiOiIyMDI0LTEyLTE4VDA5OjI0OjQ0LjYyNjQzMTYzNloiLCJhcHBfbWV0YWRhdGEiOnsicHJvdmlkZXIiOiJnb29nbGUiLCJwcm92aWRlcnMiOlsiZ29vZ2xlIl19LCJ1c2VyX21ldGFkYXRhIjp7ImF2YXRhcl91cmwiOiJodHRwczovL2xoMy5nb29nbGV1c2VyY29udGVudC5jb20vYS9BQ2c4b2NMWTBQdkRLSXo3bHVpZlZmc3d1Z0Y0WjNldzRCR19aM2R0bGFjNTFxeW1CXzJLX1JzPXM5Ni1jIiwiZW1haWwiOiJyYWFmYXRzYW1pMTAxQGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJmdWxsX25hbWUiOiJyYWFmYXQgc2FtaSIsImlzcyI6Imh0dHBzOi8vYWNjb3VudHMuZ29vZ2xlLmNvbSIsIm5hbWUiOiJyYWFmYXQgc2FtaSIsInBob25lX3ZlcmlmaWVkIjpmYWxzZSwicGljdHVyZSI6Imh0dHBzOi8vbGgzLmdvb2dsZXVzZXJjb250ZW50LmNvbS9hL0FDZzhvY0xZMFB2REtJejdsdWlmVmZzd3VnRjRaM2V3NEJHX1ozZHRsYWM1MXF5bUJfMktfUnM9czk2LWMiLCJwcm92aWRlcl9pZCI6IjExNDg1MzE1MDgyMTUwMjUzMDM0MiIsInN1YiI6IjExNDg1MzE1MDgyMTUwMjUzMDM0MiJ9LCJpZGVudGl0aWVzIjpbeyJpZGVudGl0eV9pZCI6IjE3OWY2OGU5LTdjN',
#         'Authorization.1': 'jYtNDlkZS05ZTVkLWIzOWQ4NDM2MjU3MyIsImlkIjoiMTE0ODUzMTUwODIxNTAyNTMwMzQyIiwidXNlcl9pZCI6IjM2MzhhM2E1LWI4OGUtNDBlYS04MTkyLTAzNGQyOTRjODk4MyIsImlkZW50aXR5X2RhdGEiOnsiYXZhdGFyX3VybCI6Imh0dHBzOi8vbGgzLmdvb2dsZXVzZXJjb250ZW50LmNvbS9hL0FDZzhvY0xZMFB2REtJejdsdWlmVmZzd3VnRjRaM2V3NEJHX1ozZHRsYWM1MXF5bUJfMktfUnM9czk2LWMiLCJlbWFpbCI6InJhYWZhdHNhbWkxMDFAZ21haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsImZ1bGxfbmFtZSI6InJhYWZhdCBzYW1pIiwiaXNzIjoiaHR0cHM6Ly9hY2NvdW50cy5nb29nbGUuY29tIiwibmFtZSI6InJhYWZhdCBzYW1pIiwicGhvbmVfdmVyaWZpZWQiOmZhbHNlLCJwaWN0dXJlIjoiaHR0cHM6Ly9saDMuZ29vZ2xldXNlcmNvbnRlbnQuY29tL2EvQUNnOG9jTFkwUHZES0l6N2x1aWZWZnN3dWdGNFozZXc0QkdfWjNkdGxhYzUxcXltQl8yS19Scz1zOTYtYyIsInByb3ZpZGVyX2lkIjoiMTE0ODUzMTUwODIxNTAyNTMwMzQyIiwic3ViIjoiMTE0ODUzMTUwODIxNTAyNTMwMzQyIn0sInByb3ZpZGVyIjoiZ29vZ2xlIiwibGFzdF9zaWduX2luX2F0IjoiMjAyNC0wMS0wM1QxMzo0NzoxOC44Nzk4MDlaIiwiY3JlYXRlZF9hdCI6IjIwMjQtMDEtMDNUMTM6NDc6MTguODc5ODU4WiIsInVwZGF0ZWRfYXQiOiIyMDI0LTA4LTA0VDE0OjMxOjQ0LjQyMTkzOVoiLCJlbWFpbCI6InJhYWZhdHNhbWkxMDFAZ21haWwuY29tIn1dLCJjcmVhdGVkX2F0IjoiMjAyNC0wMS0wM1QxMzo0NzoxOC44NzQ0NTlaIiwidXBkYXRlZF9hdCI6IjIwMjQtMTItMThUMDk6MjQ6NDQuNjI5NzU5WiIsImlzX2Fub255bW91cyI6ZmFsc2V9fQ',
#         'intercom-device-id-j8v9i2vs': '78127be3-c07c-470f-a31c-abaab476ebc7',
#         '_clck': 'qacu5w%7C2%7Cfrt%7C0%7C1813',
#         'AMP_MKTG_e77e0b640b': 'JTdCJTdE',
#         '_ga_CXK67KRY5M': 'GS1.1.1734517450.1.0.1734517456.0.0.0',
#         'AMP_e77e0b640b': 'JTdCJTIyZGV2aWNlSWQlMjIlM0ElMjIyNjVmMGQ4My02NjE3LTQ2ZDEtYmU4YS02OTk1ZjZjYTM5N2MlMjIlMkMlMjJ1c2VySWQlMjIlM0ElMjIzNjM4YTNhNS1iODhlLTQwZWEtODE5Mi0wMzRkMjk0Yzg5ODMlMjIlMkMlMjJzZXNzaW9uSWQlMjIlM0ExNzM0NTE3NDU0MzUyJTJDJTIyb3B0T3V0JTIyJTNBZmFsc2UlMkMlMjJsYXN0RXZlbnRUaW1lJTIyJTNBMTczNDUxNzQ2NTM2NyUyQyUyMmxhc3RFdmVudElkJTIyJTNBMjQlMkMlMjJwYWdlQ291bnRlciUyMiUzQTAlN0Q=',
#         'intercom-session-j8v9i2vs': 'KzV3ZHRIaVB0dGJGNkpjS0F4MHRxa0ZUVDdXd3l0UFF4Ny84VFprZFBocXl5Vk10R3hVLzdkOG9QTnpjMHdDcC0tZ01YZ0dTR1pWazJwOHBydEpkNjFtdz09--2462eee6bd783d639670bd95188debc11ed0c8b3',
#         '_clsk': '96n62b%7C1734517466667%7C2%7C1%7Ce.clarity.ms%2Fcollect',
#         '_ga_L9QBJH1R4M': 'GS1.1.1734517450.2.1.1734517521.0.0.0',
#     }

#     headers = {
#         'accept': '*/*',
#         'accept-language': 'ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7',
#         'baggage': 'sentry-environment=production,sentry-release=webapp%40ceb3730e4357c903046b70f158f5aaf545f9543e,sentry-public_key=6209b30caf5a49d95bb6aad90b2122e1,sentry-trace_id=b4ab150411a54d208f97e2117a1bcd2b,sentry-sample_rate=0.1,sentry-sampled=false',
#         'content-type': 'application/json',
#         # 'cookie': 'locale=en-us; cookieyes-consent=consentid:ZzB1WmRKZ0k3TGxVdUhSb1drejR5dWREYml4VlNGTWc,consent:yes,action:no,necessary:yes,functional:yes,analytics:yes,performance:yes,advertisement:yes,other:yes,lastRenewedDate:1705991862000; _ga=GA1.1.934169142.1734513863; pi_opt_in1086533=true; _gcl_au=1.1.783717375.1734513856.741403328.1734513872.1734513884; Authorization.0=base64-eyJhY2Nlc3NfdG9rZW4iOiJleUpoYkdjaU9pSklVekkxTmlJc0ltdHBaQ0k2SWxFM2JDOWlhV2hpWm1sNU9FSm5ha2dpTENKMGVYQWlPaUpLVjFRaWZRLmV5SmhZV3dpT2lKaFlXd3hJaXdpWVcxeUlqcGJleUp0WlhSb2IyUWlPaUp3WVhOemQyOXlaQ0lzSW5ScGJXVnpkR0Z0Y0NJNk1UY3pORFV4TXpnNE5IMWRMQ0poY0hCZmJXVjBZV1JoZEdFaU9uc2ljSEp2ZG1sa1pYSWlPaUpuYjI5bmJHVWlMQ0p3Y205MmFXUmxjbk1pT2xzaVoyOXZaMnhsSWwxOUxDSmhkV1FpT2lKaGRYUm9aVzUwYVdOaGRHVmtJaXdpWlcxaGFXd2lPaUp5WVdGbVlYUnpZVzFwTVRBeFFHZHRZV2xzTG1OdmJTSXNJbVY0Y0NJNk1UY3pORFl3TURJNE5Dd2lhV0YwSWpveE56TTBOVEV6T0RnMExDSnBjMTloYm05dWVXMXZkWE1pT21aaGJITmxMQ0pwYzNNaU9pSm9kSFJ3Y3pvdkwzUnVkWEI2ZUdacWNuVnJjM1ZzZG1aNVlXNXNMbk4xY0dGaVlYTmxMbU52TDJGMWRHZ3ZkakVpTENKd2FHOXVaU0k2SWlJc0luSnZiR1VpT2lKaGRYUm9aVzUwYVdOaGRHVmtJaXdpYzJWemMybHZibDlwWkNJNkltVTVPVGt3WlRNeExUZzNNakV0TkdabVpTMWlNMlprTFRnM1lUUTRNelZoTkRjd01TSXNJbk4xWWlJNklqTTJNemhoTTJFMUxXSTRPR1V0TkRCbFlTMDRNVGt5TFRBek5HUXlPVFJqT0RrNE15SXNJblZ6WlhKZmJXVjBZV1JoZEdFaU9uc2lZWFpoZEdGeVgzVnliQ0k2SW1oMGRIQnpPaTh2YkdnekxtZHZiMmRzWlhWelpYSmpiMjUwWlc1MExtTnZiUzloTDBGRFp6aHZZMHhaTUZCMlJFdEplamRzZFdsbVZtWnpkM1ZuUmpSYU0yVjNORUpIWDFvelpIUnNZV00xTVhGNWJVSmZNa3RmVW5NOWN6azJMV01pTENKamRYTjBiMjFmWTJ4aGFXMXpJanB1ZFd4c0xDSmxiV0ZwYkNJNkluSmhZV1poZEhOaGJXa3hNREZBWjIxaGFXd3VZMjl0SWl3aVpXMWhhV3hmZG1WeWFXWnBaV1FpT2lKMGNuVmxJaXdpWm5Wc2JGOXVZVzFsSWpvaWNtRmhabUYwSUhOaGJXa2lMQ0pwYzNNaU9pSm9kSFJ3Y3pvdkwyRmpZMjkxYm5SekxtZHZiMmRzWlM1amIyMGlMQ0p1WVcxbElqb2ljbUZoWm1GMElITmhiV2tpTENKd2FHOXVaVjkyWlhKcFptbGxaQ0k2SW1aaGJITmxJaXdpY0dsamRIVnlaU0k2SW1oMGRIQnpPaTh2YkdnekxtZHZiMmRzWlhWelpYSmpiMjUwWlc1MExtTnZiUzloTDBGRFp6aHZZMHhaTUZCMlJFdEplamRzZFdsbVZtWnpkM1ZuUmpSYU0yVjNORUpIWDFvelpIUnNZV00xTVhGNWJVSmZNa3RmVW5NOWN6azJMV01pTENKd2NtOTJhV1JsY2w5cFpDSTZJakV4TkRnMU16RTFNRGd5TVRVd01qVXpNRE0wTWlJc0luTjFZaUk2SWpFeE5EZzFNekUxTURneU1UVXdNalV6TURNME1pSjlmUS5aTmVJZ0JmZ2duMEw1QTRBRVRsR3c3a3lLdU5vOWR0ODh5MV9rQWRuMnJnIiwidG9rZW5fdHlwZSI6ImJlYXJlciIsImV4cGlyZXNfaW4iOjg2NDAwLCJleHBpcmVzX2F0IjoxNzM0NjAwMjg0LCJyZWZyZXNoX3Rva2VuIjoiQldLWG5WSVdwUWt5a0xJVGVVX0p3QSIsInVzZXIiOnsiaWQiOiIzNjM4YTNhNS1iODhlLTQwZWEtODE5Mi0wMzRkMjk0Yzg5ODMiLCJhdWQiOiJhdXRoZW50aWNhdGVkIiwicm9sZSI6ImF1dGhlbnRpY2F0ZWQiLCJlbWFpbCI6InJhYWZhdHNhbWkxMDFAZ21haWwuY29tIiwiZW1haWxfY29uZmlybWVkX2F0IjoiMjAyNC0wMS0wM1QxMzo0NzoxOC44ODUwNzJaIiwicGhvbmUiOiIiLCJjb25maXJtZWRfYXQiOiIyMDI0LTAxLTAzVDEzOjQ3OjE4Ljg4NTA3MloiLCJyZWNvdmVyeV9zZW50X2F0IjoiMjAyNC0wMy0xN1QxNzowNDoxMS4yMzU2NVoiLCJsYXN0X3NpZ25faW5fYXQiOiIyMDI0LTEyLTE4VDA5OjI0OjQ0LjYyNjQzMTYzNloiLCJhcHBfbWV0YWRhdGEiOnsicHJvdmlkZXIiOiJnb29nbGUiLCJwcm92aWRlcnMiOlsiZ29vZ2xlIl19LCJ1c2VyX21ldGFkYXRhIjp7ImF2YXRhcl91cmwiOiJodHRwczovL2xoMy5nb29nbGV1c2VyY29udGVudC5jb20vYS9BQ2c4b2NMWTBQdkRLSXo3bHVpZlZmc3d1Z0Y0WjNldzRCR19aM2R0bGFjNTFxeW1CXzJLX1JzPXM5Ni1jIiwiZW1haWwiOiJyYWFmYXRzYW1pMTAxQGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJmdWxsX25hbWUiOiJyYWFmYXQgc2FtaSIsImlzcyI6Imh0dHBzOi8vYWNjb3VudHMuZ29vZ2xlLmNvbSIsIm5hbWUiOiJyYWFmYXQgc2FtaSIsInBob25lX3ZlcmlmaWVkIjpmYWxzZSwicGljdHVyZSI6Imh0dHBzOi8vbGgzLmdvb2dsZXVzZXJjb250ZW50LmNvbS9hL0FDZzhvY0xZMFB2REtJejdsdWlmVmZzd3VnRjRaM2V3NEJHX1ozZHRsYWM1MXF5bUJfMktfUnM9czk2LWMiLCJwcm92aWRlcl9pZCI6IjExNDg1MzE1MDgyMTUwMjUzMDM0MiIsInN1YiI6IjExNDg1MzE1MDgyMTUwMjUzMDM0MiJ9LCJpZGVudGl0aWVzIjpbeyJpZGVudGl0eV9pZCI6IjE3OWY2OGU5LTdjN; Authorization.1=jYtNDlkZS05ZTVkLWIzOWQ4NDM2MjU3MyIsImlkIjoiMTE0ODUzMTUwODIxNTAyNTMwMzQyIiwidXNlcl9pZCI6IjM2MzhhM2E1LWI4OGUtNDBlYS04MTkyLTAzNGQyOTRjODk4MyIsImlkZW50aXR5X2RhdGEiOnsiYXZhdGFyX3VybCI6Imh0dHBzOi8vbGgzLmdvb2dsZXVzZXJjb250ZW50LmNvbS9hL0FDZzhvY0xZMFB2REtJejdsdWlmVmZzd3VnRjRaM2V3NEJHX1ozZHRsYWM1MXF5bUJfMktfUnM9czk2LWMiLCJlbWFpbCI6InJhYWZhdHNhbWkxMDFAZ21haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsImZ1bGxfbmFtZSI6InJhYWZhdCBzYW1pIiwiaXNzIjoiaHR0cHM6Ly9hY2NvdW50cy5nb29nbGUuY29tIiwibmFtZSI6InJhYWZhdCBzYW1pIiwicGhvbmVfdmVyaWZpZWQiOmZhbHNlLCJwaWN0dXJlIjoiaHR0cHM6Ly9saDMuZ29vZ2xldXNlcmNvbnRlbnQuY29tL2EvQUNnOG9jTFkwUHZES0l6N2x1aWZWZnN3dWdGNFozZXc0QkdfWjNkdGxhYzUxcXltQl8yS19Scz1zOTYtYyIsInByb3ZpZGVyX2lkIjoiMTE0ODUzMTUwODIxNTAyNTMwMzQyIiwic3ViIjoiMTE0ODUzMTUwODIxNTAyNTMwMzQyIn0sInByb3ZpZGVyIjoiZ29vZ2xlIiwibGFzdF9zaWduX2luX2F0IjoiMjAyNC0wMS0wM1QxMzo0NzoxOC44Nzk4MDlaIiwiY3JlYXRlZF9hdCI6IjIwMjQtMDEtMDNUMTM6NDc6MTguODc5ODU4WiIsInVwZGF0ZWRfYXQiOiIyMDI0LTA4LTA0VDE0OjMxOjQ0LjQyMTkzOVoiLCJlbWFpbCI6InJhYWZhdHNhbWkxMDFAZ21haWwuY29tIn1dLCJjcmVhdGVkX2F0IjoiMjAyNC0wMS0wM1QxMzo0NzoxOC44NzQ0NTlaIiwidXBkYXRlZF9hdCI6IjIwMjQtMTItMThUMDk6MjQ6NDQuNjI5NzU5WiIsImlzX2Fub255bW91cyI6ZmFsc2V9fQ; intercom-device-id-j8v9i2vs=78127be3-c07c-470f-a31c-abaab476ebc7; _clck=qacu5w%7C2%7Cfrt%7C0%7C1813; AMP_MKTG_e77e0b640b=JTdCJTdE; _ga_CXK67KRY5M=GS1.1.1734517450.1.0.1734517456.0.0.0; AMP_e77e0b640b=JTdCJTIyZGV2aWNlSWQlMjIlM0ElMjIyNjVmMGQ4My02NjE3LTQ2ZDEtYmU4YS02OTk1ZjZjYTM5N2MlMjIlMkMlMjJ1c2VySWQlMjIlM0ElMjIzNjM4YTNhNS1iODhlLTQwZWEtODE5Mi0wMzRkMjk0Yzg5ODMlMjIlMkMlMjJzZXNzaW9uSWQlMjIlM0ExNzM0NTE3NDU0MzUyJTJDJTIyb3B0T3V0JTIyJTNBZmFsc2UlMkMlMjJsYXN0RXZlbnRUaW1lJTIyJTNBMTczNDUxNzQ2NTM2NyUyQyUyMmxhc3RFdmVudElkJTIyJTNBMjQlMkMlMjJwYWdlQ291bnRlciUyMiUzQTAlN0Q=; intercom-session-j8v9i2vs=KzV3ZHRIaVB0dGJGNkpjS0F4MHRxa0ZUVDdXd3l0UFF4Ny84VFprZFBocXl5Vk10R3hVLzdkOG9QTnpjMHdDcC0tZ01YZ0dTR1pWazJwOHBydEpkNjFtdz09--2462eee6bd783d639670bd95188debc11ed0c8b3; _clsk=96n62b%7C1734517466667%7C2%7C1%7Ce.clarity.ms%2Fcollect; _ga_L9QBJH1R4M=GS1.1.1734517450.2.1.1734517521.0.0.0',
#         'origin': 'https://app.magicschool.ai',
#         'priority': 'u=1, i',
#         'referer': 'https://app.magicschool.ai/tools/mc-assessment',
#         'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
#         'sec-ch-ua-mobile': '?0',
#         'sec-ch-ua-platform': '"Windows"',
#         'sec-fetch-dest': 'empty',
#         'sec-fetch-mode': 'cors',
#         'sec-fetch-site': 'same-origin',
#         'sentry-trace': 'b4ab150411a54d208f97e2117a1bcd2b-beda308987ea4432-0',
#         'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
#     }

#     json_data = {
#         'slug': 'mc-assessment',
#         'locale': 'en-us',
#         'inputs': {
#             'gradeLevel': grade_level,
#             'numQuestions': str(num_questions),
#             'topic': {
#                 'files': [],
#                 'text': str(topic),
#             },
#         },
#     }

#     response = requests.post('https://app.magicschool.ai/api/generations', cookies=cookies, headers=headers, json=json_data)

#     print(response.text)
#     parsed_data = parse_quiz_text(response.text)

#     # Convert the parsed data to JSON
#     quiz_json = json.dumps(parsed_data, indent=4)
#     data = quiz_json
#     print(data)
#     return data

# def get_combined_data(num_questions, topic):
#     # Get data for both grade levels
#     university_data = get_questions(num_questions, topic, 'university')
#     # professional_staff_data = get_questions(num_questions, topic, 'professional-staff')
    
#     # # Combine the data
#     # combined_data = {}
#     # if university_data:
#     #     combined_data['university'] = university_data
#     # if professional_staff_data:
#     #     combined_data['professional-staff'] = professional_staff_data
#     # print(combined_data)
#     return university_data


def get_questions(topic, num_questions):
    import requests

    cookies = {
        'AMP_MKTG_70a5be3710': 'JTdCJTdE',
        'AMP_70a5be3710': 'JTdCJTIyZGV2aWNlSWQlMjIlM0ElMjJhMzA0ODk0OS05MWIwLTQ1OTMtYjU5MC04OTQ1NThiOWFiMTIlMjIlMkMlMjJzZXNzaW9uSWQlMjIlM0ExNzM0ODAxMjg3NDc0JTJDJTIyb3B0T3V0JTIyJTNBZmFsc2UlMkMlMjJsYXN0RXZlbnRUaW1lJTIyJTNBMTczNDgwMTI4NzQ3OSUyQyUyMmxhc3RFdmVudElkJTIyJTNBMiU3RA==',
        '__client_uat': '0',
        '__client_uat_wYOPO35R': '0',
        'crisp-client%2Fsession%2Ffaab0820-f408-4327-915b-bc17f2332d39': 'session_92021fc7-4cf5-4b64-b5fe-82d6f3e1874c',
        '__stripe_mid': '0d785786-3f51-48e0-aa0a-cdb754b7a83a4809ce',
        '__stripe_sid': '9454cd36-334d-4ee8-a53e-faa4e76a9b170c32eb',
    }

    headers = {
        'accept': '*/*',
        'accept-language': 'ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7',
        'baggage': 'sentry-environment=vercel-production,sentry-release=69b2b1c3f422dff6472132d59e8581489aa8427a,sentry-public_key=f6bbb7b197a2a7e09bc25634f533bdeb,sentry-trace_id=8d0baca7f0634408bfce0e8857294d98',
        'content-type': 'application/json',
        # 'cookie': 'AMP_MKTG_70a5be3710=JTdCJTdE; AMP_70a5be3710=JTdCJTIyZGV2aWNlSWQlMjIlM0ElMjJhMzA0ODk0OS05MWIwLTQ1OTMtYjU5MC04OTQ1NThiOWFiMTIlMjIlMkMlMjJzZXNzaW9uSWQlMjIlM0ExNzM0ODAxMjg3NDc0JTJDJTIyb3B0T3V0JTIyJTNBZmFsc2UlMkMlMjJsYXN0RXZlbnRUaW1lJTIyJTNBMTczNDgwMTI4NzQ3OSUyQyUyMmxhc3RFdmVudElkJTIyJTNBMiU3RA==; __client_uat=0; __client_uat_wYOPO35R=0; crisp-client%2Fsession%2Ffaab0820-f408-4327-915b-bc17f2332d39=session_92021fc7-4cf5-4b64-b5fe-82d6f3e1874c; __stripe_mid=0d785786-3f51-48e0-aa0a-cdb754b7a83a4809ce; __stripe_sid=9454cd36-334d-4ee8-a53e-faa4e76a9b170c32eb',
        'origin': 'https://www.heuristi.ca',
        'priority': 'u=1, i',
        'referer': 'https://www.heuristi.ca/tools/free-ai-quiz-generator',
        'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'sentry-trace': '8d0baca7f0634408bfce0e8857294d98-8ca3ef1a40dafdf7',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    }

    json_data = {
        'operation': 'quiz-from-text',
        'input': topic,
        'language': 'English',
        'count': str(num_questions),
    }

    response = requests.post('https://www.heuristi.ca/api/free-flashcard-generator',cookies=cookies headers=headers, json=json_data)
    return response.json()

