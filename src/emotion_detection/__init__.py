"""Emotion Detection Package"""
from .facial_emotion import FacialEmotionDetector
from .audio_emotion import AudioEmotionDetector
from .text_emotion import TextEmotionDetector

__all__ = ['FacialEmotionDetector', 'AudioEmotionDetector', 'TextEmotionDetector']
