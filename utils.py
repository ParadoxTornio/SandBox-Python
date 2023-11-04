def custom_collision(sprite1, sprite2):
    if sprite1 != sprite2:
        return sprite1.rect.colliderect(sprite2.rect)
    return False
