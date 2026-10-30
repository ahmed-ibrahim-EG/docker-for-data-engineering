# 1. Base Image: رسمية وخفيفة
FROM python:3.11-slim

# 2. متغيرات بيئة لتحسين الأداء
#    - PYTHONDONTWRITEBYTECODE: يمنع إنشاء ملفات .pyc
#    - PYTHONUNBUFFERED: يظهر الـ logs فورًا بدون buffering
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# 3. مجلد العمل
WORKDIR /app

# 4. Layer Caching: انسخ requirements.txt وثبّت الحزم أولًا
COPY requirements.txt .
RUN pip install -r requirements.txt

# 5. انسخ باقي الكود (الطبقة دي بتتغير كتير، فبتتحط في الآخر)
COPY . .

# 6. البورت الافتراضي لـ Flask
EXPOSE 5000

# 7. ENTRYPOINT للأمر الثابت، و CMD للملف (Exec Form / JSON Array)
ENTRYPOINT ["python"]
CMD ["app.py"]