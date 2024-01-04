# category_conversion.py
# supercategoryID = ['공통']인 것에 (119562, 118920)->238482, (119564, 118922)->238486, (157054, 118926)->275980
# 받은 detection_category를 categoryID로 바꿔주는데, video_subject에 따라서 다르게 바꿔줍니다.


def convert_category(detection_category, video_subject):
    if video_subject == 1:
        # Mapping for video_subject = 1 (고양이)
        mapping = {2: 118920, 3: 118923, 4: 119567, 5: 119567, 6: 119571, 7: 119562, 8: 119564, 9: 157054}
    elif video_subject == 0:
        # Mapping for video_subject = 0 (강아지)
        mapping = {2: 118920, 3: 118923, 4: 119567, 5: 119567, 6: 119571, 7: 118920, 8: 118922, 9: 118926}
    else:
        # Mapping for video_subject = -1 (공통)
        mapping = {2: 118920, 3: 118923, 4: 119567, 5: 119567, 6: 119571, 7: 238482, 8: 238486, 9: 275980}
    
    return mapping.get(detection_category)
