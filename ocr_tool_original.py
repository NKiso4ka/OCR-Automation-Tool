import easyocr
import os
import cv2
import numpy as np

def sozdat_text(image_path):
   #Распознает текст с изображения с обработкой ошибок
    try:
        #Проверяет файл
        if not os.path.exists(image_path):
            return f" Файл {image_path} не найден!"
        
        print(f" Обрабатываю: {image_path}")
        
        #ПРЕДВАРИТЕЛЬНАЯ ОБРАБОТКА ИЗОБРАЖЕНИЯ
        print("Предобработка изображения...")
        img = cv2.imread(image_path)
        
        if img is None:
            return " Не удалось загрузить изображение!"
        
        #Проверяет размер изображения
        height, width = img.shape[:2]
        print(f" Размер изображения: {width}x{height}")
        
        #Если изображение слишком маленькое - увеличивает
        if width < 50 or height < 50:
            print("Увеличиваю размер изображения...")
            scale = 4
            new_width = width * scale
            new_height = height * scale
            img = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_CUBIC)
        
        #Улучшает качество изображения
        #Конвертирует в grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        #Увеличивает контраст
        contrast = cv2.equalizeHist(gray)
        
        #Убирает шум
        denoised = cv2.medianBlur(contrast, 3)
        
        #Сохраняет обработанное изображение
        cv2.imwrite('processed_image.jpg', denoised)
        print("Изображение обработано и сохранено как 'processed_image.jpg'")
        
        #Загружает EasyOCR
        print(" Загружаем EasyOCR...")
        reader = easyocr.Reader(['ru', 'en'])
        
        #Распознает текст с обработанного изображения
        print(" Распознаем текст...")
        results = reader.readtext('processed_image.jpg')
        
        #Извлекает текст
        text = ' '.join([result[1] for result in results])
        
        print(f" Распознано {len(results)} элементов")
        return text
        
    except Exception as e:
        return f" Ошибка: {str(e)}"

#Альтернативная версия с более простой обработкой
def sozdat_text_simple(image_path):
    try:
        if not os.path.exists(image_path):
            return f" Файл {image_path} не найден!"
        
        print(f" Обрабатываю: {image_path}")
        
        # Просто загружаем и сразу распознаем
        reader = easyocr.Reader(['ru', 'en'])
        results = reader.readtext(image_path)
        
        text = ' '.join([result[1] for result in results])
        print(f"Распознано {len(results)} элементов")
        return text
        
    except Exception as e:
        return f" Ошибка: {str(e)}"

#Версия с попыткой разных подходов
def sozdat_text_robust(image_path):
    
    try:
        if not os.path.exists(image_path):
            return f" Файл {image_path} не найден!"
        
        print(f" Обрабатываю: {image_path}")
        reader = easyocr.Reader(['ru', 'en'])
        
        #Рразные подходы, если прошлые не получатся
        methods = [
            lambda: reader.readtext(image_path),  #Прямое чтение
            lambda: reader.readtext(cv2.imread(image_path)),  #Через OpenCV
        ]
        
        results = None
        for i, method in enumerate(methods):
            try:
                print(f"Попытка {i+1}...")
                results = method()
                if results:
                    print(f" Успех с методом {i+1}")
                    break
            except Exception as e:
                print(f" Метод {i+1} не сработал: {e}")
                continue
        
        if not results:
            return " Не удалось распознать текст ни одним методом"
        
        text = ' '.join([result[1] for result in results])
        print(f"Распознано {len(results)} элементов")
        return text
        
    except Exception as e:
        return f"Ошибка: {str(e)}"

if __name__ == "__main__":
    print("Запуск распознавания текста...")
    
    #Пробует разные методы
    file_to_process = 'Screenshot.jpg'
    
    if not os.path.exists(file_to_process):
        print(" Файл не найден! Доступные файлы:")
        for file in os.listdir('.'):
            if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                print(f"   - {file}")
    else:
        print("1. Пробуем упрощенный метод...")
        text = sozdat_text_simple(file_to_process)
        
        if text and not text.startswith(''):
            print("\n" + "="*50)
            print("РЕЗУЛЬТАТ:")
            print("="*50)
            print(text)
            
            #Сохранение
            with open('result.txt', 'w', encoding='utf-8') as f:
                f.write(text)
            print("="*50)
            print("Сохранено в 'result.txt'")
        else:
            print(f"Упрощенный метод не сработал: {text}")
            print("\n2. Пробуем метод с обработкой изображения...")
            text = sozdat_text(file_to_process)
            
            if text and not text.startswith('Х'):
                print("\n" + "="*50)
                print("РЕЗУЛЬТАТ (с обработкой):")
                print("="*50)
                print(text)
                
                with open('result_processed.txt', 'w', encoding='utf-8') as f:
                    f.write(text)
                print("="*50)
                print("Сохранено в 'result_processed.txt'")
