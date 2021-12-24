from pygame import Rect

def collide_with(collider: Rect, collisions: list[Rect]) -> bool:
    return any([collider.colliderect(x) for x in collisions])
