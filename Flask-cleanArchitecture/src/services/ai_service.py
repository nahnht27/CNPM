import os
from datetime import datetime

import requests


class AIService:
    def __init__(self, repository):
        self.repository = repository

        self.api_url = os.getenv('AI_API_URL')
        self.api_key = os.getenv('AI_API_KEY')
        self.model = os.getenv('AI_MODEL')

    def ask_ai(self, **data):
        user_id = data.get('user_id')
        interaction_type = data.get('interaction_type', 'question')
        query_text = data.get('query_text')

        if not query_text:
            raise ValueError('Query text is required')

        if not self.api_url:
            raise ValueError('AI_API_URL is not configured')

        if not self.api_key:
            raise ValueError('AI_API_KEY is not configured')

        if not self.model:
            raise ValueError('AI_MODEL is not configured')

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}'
        }

        payload = {
            'model': self.model,
            'messages': [
                {
                    'role': 'system',
                    'content': (
                        'Bạn là trợ lý AI hỗ trợ cộng đồng nhiếp ảnh phim. '
                        'Hãy trả lời các câu hỏi, tìm kiếm thông tin và đưa ra '
                        'gợi ý liên quan đến nhiếp ảnh phim, phòng tối, '
                        'phòng chụp, thiết bị và kỹ thuật chụp ảnh.'
                    )
                },
                {
                    'role': 'user',
                    'content': query_text
                }
            ]
        }

        response = requests.post(
            self.api_url,
            headers=headers,
            json=payload,
            timeout=60
        )

        if response.status_code != 200:
            raise ValueError(
                f'AI API request failed: {response.text}'
            )

        result = response.json()

        response_text = self._extract_response(result)

        log_data = {
            'user_id': user_id,
            'interaction_type': interaction_type,
            'query_text': query_text,
            'response_text': response_text,
            'created_at': datetime.now()
        }

        self.repository.add(log_data)

        return {
            'user_id': user_id,
            'interaction_type': interaction_type,
            'query_text': query_text,
            'response_text': response_text,
            'created_at': log_data['created_at']
        }

    def _extract_response(self, result):
        """
        Lấy nội dung câu trả lời từ response
        của AI API theo định dạng OpenAI-compatible.
        """

        try:
            return result['choices'][0]['message']['content']
        except (KeyError, IndexError, TypeError):
            raise ValueError('Invalid response from AI API')