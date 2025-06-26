def run_tests(window, player):
    # test_collision(window)
    # Test death with X key, will be removed when fatal objects or enemies are added
    if player:
        player.death_test()