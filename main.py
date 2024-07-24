import pygame
from sys import exit

# Initialization ---

pygame.init()

bounds = [1280, 720]
main_window = pygame.display.set_mode(bounds)
fps: int = 60
clock = pygame.time.Clock()

spawn_coords = (100, 720 - 100)
tile_size = 50

timer1_cooldown = 3

background = pygame.image.load("background.png").convert_alpha()
background = pygame.transform.rotozoom(background, 90, 1)


# Classes ---

class Segment(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.direc = 0  # 0 up, 1 right, 2 down, 3 left

        self.next_segment: Segment = None
        self.prev_segment: Segment = None

        self.prev_position = [0, 0]
        self.prev_direc = 0

    def get_next_segment(self):
        return self.next_segment

    def get_prev_segment(self):
        return self.prev_segment

    def set_position(self, pos: list):
        self.rect.center = pos

    def get_position(self):
        return self.rect.center

    def get_prev_position(self):
        return self.prev_position

    def get_prev_direc(self):
        return self.prev_direc

    def move(self):
        self.prev_position = self.get_position()
        self.prev_direc = self.direc
        if self.direc == 0:
            self.image = pygame.transform.rotate(self.main_image, 0)
            self.rect.centery = int(self.rect.centery - tile_size)
        elif self.direc == 1:
            self.image = pygame.transform.rotate(self.main_image, 270)
            self.rect.centerx = int(self.rect.centerx + tile_size)
        elif self.direc == 2:
            self.image = pygame.transform.rotate(self.main_image, 180)
            self.rect.centery = int(self.rect.centery + tile_size)
        elif self.direc == 3:
            self.image = pygame.transform.rotate(self.main_image, 90)
            self.rect.centerx = int(self.rect.centerx - tile_size)


    def shift(self):

        # TODO implement in head
        self.prev_position = self.get_position()
        print(f"UNTailed |{self.tail_number}|<-{self.prev_segment.tail_number}")
        self.set_position(self.prev_segment.get_prev_position())
        self.set_direc(self.prev_segment.get_prev_direc())
        print(f"{self.prev_direc} to {self.direc}")
        self.correct_direc()

        self.tail_number -= 1

        if(head.last_segment == self):
            head.last_segment = self.prev_segment

        if(self.next_segment != None):
            self.next_segment.shift()

    def correct_direc(self):
        if self.direc == 0:
            self.image = pygame.transform.rotate(self.main_image, 0)
        elif self.direc == 1:
            self.image = pygame.transform.rotate(self.main_image, 270)
        elif self.direc == 2:
            self.image = pygame.transform.rotate(self.main_image, 180)
        elif self.direc == 3:
            self.image = pygame.transform.rotate(self.main_image, 90)

    def set_direc(self, dir: int):
        self.prev_direc = self.direc
        if dir < 4 and dir >= 0:
            self.direc = dir

    def get_direc(self):
        return self.direc

    def add_segment(self):  # Works like insertion at head + 1 position of doubly linked list
        head.tail_count += 1

        segment = Tail()
        print("ok bro")
        segment.set_position(self.get_prev_position())
        segment.set_direc(self.get_direc())
        segment.correct_direc()

        self.next_segment = segment
        head.last_segment = segment

        tail_group.add((segment))

    def kill_segment(self):  # Works like insertion at head + 1 position of doubly linked list
        head.tail_count -= 1
        print("done bro")

        self.next_segment.prev_segment = self.prev_segment
        self.prev_segment.next_segment = self.next_segment

        self.shift()
        tail_group.remove(self)

    def update(self):
        pass


class Head(Segment):
    def __init__(self):
        super().__init__()
        self.main_image = pygame.image.load("head.png")
        self.main_image = pygame.transform.scale(self.main_image, [50, 50])
        self.image = self.main_image
        self.rect = self.main_image.get_rect(center=spawn_coords)

        self.tick_timer = 0
        self.timer1 = 0
        self.tail_timer = 0
        self.last_segment: Segment = self

        self.tail_count = 0
        self.tail_number = self.tail_count

    def player_input(self):
        if self.tick_timer >= 12:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w] and not keys[pygame.K_a] and not keys[pygame.K_s] and not keys[
                pygame.K_d] and self.direc != 2:
                self.set_direc(0)
                self.trigger_tick()
            elif not keys[pygame.K_w] and not keys[pygame.K_a] and not keys[pygame.K_s] and keys[
                pygame.K_d] and self.direc != 3:
                self.set_direc(1)
                self.trigger_tick()
            elif not keys[pygame.K_w] and not keys[pygame.K_a] and keys[pygame.K_s] and not keys[
                pygame.K_d] and self.direc != 0:
                self.set_direc(2)
                self.trigger_tick()
            elif not keys[pygame.K_w] and keys[pygame.K_a] and not keys[pygame.K_s] and not keys[
                pygame.K_d] and self.direc != 1:
                self.set_direc(3)
                self.trigger_tick()
            if keys[pygame.K_SPACE]:
                self.trigger_tick()
                self.add_segment_handler()

    def set_next_segment(self, segment: Segment):
        self.next_segment = segment

    def set_prev_segment(self, segment: Segment):
        self.prev_segment = segment

    def add_segment_handler(self):  # Works like insertion at head + 1 position of doubly linked list
        if self.tail_timer >= timer1_cooldown:
            self.last_segment.add_segment()
            self.tail_timer = 0

    def trigger_tick(self):
        self.tick_timer = 0
        self.timer1 += 1
        self.tail_timer += 1

        for segment in player_group:
            segment.move()
        for segment in tail_group:
            segment.move()

        if self.timer1 >= timer1_cooldown:
            #self.add_segment_handler()
            self.timer1 = 0
        print(self.tail_count)

    def update(self):
        self.player_input()
        self.tick_timer += 1
        if self.tick_timer >= fps:
            print(self.rect.center)
            self.trigger_tick()


class Tail(Segment):
    def __init__(self):
        super().__init__()
        self.main_image = pygame.image.load("body.png")
        self.main_image = pygame.transform.scale(self.main_image, [50, 50])
        self.rot = pygame.image.load("rotbody.png")
        self.rot = pygame.transform.scale(self.main_image, [50, 50])
        self.image = self.main_image
        self.rect = self.main_image.get_rect(center=[0, 0])

        self.prev_segment: Segment = head.last_segment
        head.set_next_segment(self)

        self.tail_number = head.tail_count

    def set_next_segment(self, segment: Segment):
        self.next_segment = segment

    def set_prev_segment(self, segment: Segment):
        self.prev_segment = segment

    def correct_direc(self):
        if self.direc == self.prev_segment.prev_direc:
            if self.direc == 0:
                self.image = pygame.transform.rotate(self.main_image, 0)
            elif self.direc == 1:
                self.image = pygame.transform.rotate(self.main_image, 270)
            elif self.direc == 2:
                self.image = pygame.transform.rotate(self.main_image, 180)
            elif self.direc == 3:
                self.image = pygame.transform.rotate(self.main_image, 90)
        else:
            if (self.direc == 0 and self.prev_segment.prev_direc == 1) or (
                    self.direc == 3 and self.prev_segment.prev_direc == 2):
                self.image = pygame.transform.rotate(self.main_image, 315)

    def move(self):
        # TODO basic movement, and diagonal check if segment is a corner, if so use diagonal image set, later change to hex coords
        self.prev_position = self.get_position()
        print(f"UNTailed |{self.tail_number}|<-{self.prev_segment.tail_number}")
        self.set_position(self.prev_segment.get_prev_position())
        self.set_direc(self.prev_segment.get_prev_direc())
        print(f"{self.prev_direc} to {self.direc}")
        self.correct_direc()

        # Kill sequence
        if (self.rect.centerx < -tile_size) or (self.rect.centerx > bounds[0] + tile_size) or (
                self.rect.centery < -tile_size) or (self.rect.centery > bounds[1] + tile_size):
            self.kill()


# Initialization 2 ---

head = Head()
player_group = pygame.sprite.GroupSingle(head)

tail_group = pygame.sprite.Group()

# Game Loop ---

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    # ---
    main_window.blit(background, (0, 0))
    player_group.update()
    player_group.draw(main_window)
    tail_group.update()
    tail_group.draw(main_window)

    # ---
    pygame.display.update()
    clock.tick(fps)
