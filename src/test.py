from src.collision import rect1, rect2, CollisionRect


# collision test, will be removed at some point
def test_collision(window):
    for obj in CollisionRect.all_objects:
        obj.check_collision()
        obj.draw(window)

    rect1.move_towards(rect2, speed=2)
    rect2.move_towards(rect1, speed=2)

def run_tests(window, player):
    # test_collision(window)
    # Test death with X key, will be removed when fatal objects or enemies are added
    if player:
        player.death_test()