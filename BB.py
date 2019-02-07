from tkinter import *
import time
import random
import winsound


class Game(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title("Brick Breaker; From Python - Deluxe")
        self._draw()
        pass;

    def _draw(self):
        global canvas, paddle, ball, sky, start_time, bricks
        canvas = Canvas(self, width=600, height=450, bd=0, highlightthickness=0)
        canvas.pack()
        self.update()

        ground = canvas.create_rectangle(0, 0, canvas.winfo_width(), canvas.winfo_height() * 0.15, fill='#85754E',
                                         outline='black')
        canvas.move(ground, 0, canvas.winfo_height() * 0.85)
        x = 0.05
        for i in range(0, 18):
            canvas.create_line(canvas.winfo_width() * x, canvas.winfo_height() * 0.85, canvas.winfo_width() * x + 20,
                               canvas.winfo_height() * 0.8 + 50)
            x += 0.05

        sky = self._night_sky()
        paddle = Paddle(canvas)
        ball = Ball(canvas, paddle)
        bricks = Bricks(canvas, ball)

        start_time = 0

        self._play()
        pass

    def _play(self):

        while 1:
            if ball.gameOver:
                break
            paddle._draw()
            ball._draw()
            sky._draw()
            bricks._draw()
            self.update_idletasks()
            self.update()
            time.sleep(0.01)

        self._gameOver()

    def _gameOver(self):
        global instructs
        canvas.create_rectangle(0, 0, 600, 450, fill='#E77200')
        canvas.config(background='black')
        canvas.create_text(600 / 2, 450 / 2, text="Game Over!", font=("comic sans ms", 48, "bold"),
                           fill="white")

        instructs = Label(self, text="Press 'space' key to restart", background="white",
                          font=("comic sans ms", 12, "normal"))
        instructs.pack(side=BOTTOM)
        self.config(background="white")
        canvas.bind_all("<KeyPress-space>", self._restart)
        winsound.Beep(1000,3)

    def _restart(self, event):
        if event.keysym == 'space':
            instructs.destroy()
            canvas.destroy()
            self._draw()

    def _night_sky(self):
        canvas.config(background="black")
        start_time = time.time()
        for i in range(0, 20):
            canvas.move(self._create_star('white', 5), random.randint(0, 600), random.randint(0, 300))

        return Moon(canvas, start_time)

    def _create_star(self, color, shrink):
        points = [100, 140, 110, 110, 140, 100, 110, 90, 100, 60, 90, 90, 60, 100, 90, 110]
        for p in range(0, len(points)):
            points[p] = points[p] / shrink
        return canvas.create_polygon(points, fill=color)


class Ball:
    def __init__(self, canvas, paddle,):
        self.canvas = canvas
        self.id = canvas.create_oval(0, 0, 24, 24, fill='red')
        self.dot = canvas.create_oval(0, 0, 4, 4, fill='black')
        self.canvas_width = self.canvas.winfo_width()
        self.canvas_height = self.canvas.winfo_height()
        self.canvas.move(self.id, self.canvas_width * 0.4 + 40, self.canvas_height * 0.76)
        self.canvas.move(self.dot, self.canvas_width * 0.492, self.canvas_height * 0.77)
        self.gameOver = False
        starts = [-3, -2, -1, 0, 1, 2, 3]
        random.shuffle(starts)
        self.x = starts[0]
        self.y = -3
        self.paddle = paddle
        pass

    def _draw(self):
        self.canvas.move(self.id, self.x, self.y)
        self.canvas.move(self.dot, self.x, self.y)
        pos = self.canvas.coords(self.id)
        if pos[1] <= 0:
            self.y = +3
        if pos[3] >= self.canvas_height:
            # self.y = -3
            self.gameOver = True
        if self._hit_paddle(pos) == 1:
            self.y = -3
            winsound.Beep(3000, 1)
        if self._hit_paddle(pos) == 2:
            self.y = +3
            winsound.Beep(3000, 1)
        if pos[0] <= 0:
            self.x = +3
        if pos[2] >= self.canvas_width:
            self.x = -3

        pass

    def _hit_paddle(self, ball_pos):
        pad_pos = self.canvas.coords(self.paddle.id)

        if ball_pos[2] >= pad_pos[6] and ball_pos[0] <= pad_pos[16]:
            if ball_pos[3] >= pad_pos[11] and ball_pos[3] <= pad_pos[1]:
                return 1
        if ball_pos[2] >= pad_pos[6] and ball_pos[0] <= pad_pos[16]:
            if ball_pos[1] <= pad_pos[1] and ball_pos[1] >= pad_pos[11]:
                return 2
        return 0


class Paddle:
    def __init__(self, canvas):
        self.canvas = canvas
        self.id = canvas.create_polygon(25, 12, 20, 20, 15, 12, 0, 10, 3, 5, 15, 0, 90, 0, 102, 5, 105, 10, 90, 12, 85,
                                        20, 80,
                                        12, fill='#2E5894')
        self.canvas_width = self.canvas.winfo_width()
        self.canvas_height = self.canvas.winfo_height()
        self.canvas.move(self.id, self.canvas_width * 0.4, self.canvas_height * 0.85 - 17)
        self.x = 0
        self.rel = False

        self.canvas.bind_all("<KeyPress-Left>", self._move_left)
        self.canvas.bind_all("<KeyPress-Right>", self._move_ryt)

        self.canvas.bind_all("<KeyRelease-Left>", self._check_release)
        self.canvas.bind_all("<KeyRelease-Right>", self._check_release)
        pass

    def _move_left(self, event):

        if self.rel:
            self.x = -2
            self.rel = False
        else:
            self.x -= 0.05

    def _move_ryt(self, event):
        if self.rel:
            self.x = +2
            self.rel = False
        else:
            self.x += 0.05

    def _check_release(self, event):
        self.rel = True

    def _draw(self):
        self.canvas.move(self.id, self.x, 0)
        pos = self.canvas.coords(self.id)
        if pos[6] <= 0:
            self.x = 0
        elif pos[16] >= self.canvas_width:
            self.x = 0
        pass


class Moon:
    def __init__(self, canvas, start_time):
        self.canvas = canvas
        self.start_time = start_time
        self.id = canvas.create_oval(0, 0, 48, 48, fill='#F0F0F0')
        self.shape = canvas.create_oval(0, 0, 32, 32, fill='black')

        self.canvas_width = self.canvas.winfo_width()
        self.canvas_height = self.canvas.winfo_height()
        self.canvas.move(self.id, self.canvas_width * 0.9, self.canvas_height * 0.1)
        self.canvas.move(self.shape, self.canvas_width * 0.9, self.canvas_height * 0.1)
        self.sum_point = -0.3

        self.x = 0
        self.y = 0
        pass

    def _draw(self):
        self.canvas.move(self.id, self.x, self.y)
        self.canvas.move(self.shape, self.x, self.y)
        pos = self.canvas.coords(self.id)

        if pos[0] <= 0:
            self.sum_point = 0.3
        elif pos[2] >= self.canvas_width:
            self.sum_point = -0.3
        if 5 < time.time() - self.start_time < 10:
            self.x = self.sum_point
        elif time.time() - self.start_time > 10:
            self.x = 0
            self.start_time = time.time()


class Bricks:
    def __init__(self, canvas, ball):
        self.canvas = canvas
        self.canvas_width = canvas.winfo_width()
        self.canvas_height = canvas.winfo_height()
        self.id = []
        row_count = 10
        self.brick_arr = 0

        spacing_x = 10
        spacing_y = 10
        vv = 62
        xx = 10
        for x in range(0, 6):
            self.id.append(self._create_brick('yellow'))
            self.canvas.move(self.id[self.brick_arr], spacing_x, spacing_y)
            self.brick_arr += 1
            spacing_x += 52
            spacing_y += 32
            for y in range(0, row_count):
                self.id.append(self._create_brick('red'))
                self.canvas.move(self.id[self.brick_arr], vv, xx)
                self.brick_arr += 1
                vv += 52

            row_count -= 2
            xx += 32
            vv = 62 + spacing_x - 10

    def _create_brick(self, color):
        return self.canvas.create_polygon(0, 0, 5, -5, 45, -5, 50, 0, 50, 20, 45, 25, 5, 25, 0, 20, fill=color,
                                          outline='black')

    def _draw(self):
        count = 0
        for brick in self.id:
            brick_pos = self.canvas.coords(brick)
            ball_pos = self.canvas.coords(ball.id)
            # x1,y1,x2,y2
            # 0, 1, 2 , 3
            try:
                if ball_pos[1] <= brick_pos[13] and ball_pos[1] >= brick_pos[3]:
                    if ball_pos[0] >= brick_pos[14] and ball_pos[0] <= brick_pos[8]:
                        ball.y = +3
                        self.canvas.delete(brick)
                        del (self.id[count])
                        winsound.Beep(2000, 1)
                elif ball_pos[1] <= brick_pos[13] and ball_pos[1] >= brick_pos[3]:
                    if ball_pos[2] >= brick_pos[14] and ball_pos[2] <= brick_pos[8]:
                        ball.y = +3
                        self.canvas.delete(brick)
                        del (self.id[count])
                        winsound.Beep(2000, 1)

                elif ball_pos[3] >= brick_pos[1] and ball_pos[3] <= brick_pos[15]:
                    if ball_pos[0] >= brick_pos[0] and ball_pos[0] <= brick_pos[6]:
                        ball.y = +3
                        self.canvas.delete(brick)
                        del (self.id[count])
                        winsound.Beep(2000, 1)

                elif ball_pos[3] >= brick_pos[1] and ball_pos[3] <= brick_pos[15]:
                    if ball_pos[2] >= brick_pos[6] and ball_pos[2] <= brick_pos[0]:
                        ball.y = +3
                        self.canvas.delete(brick)
                        del (self.id[count])
                        winsound.Beep(2000, 1)
                count += 1
            except IndexError:
                print("Error")


def main():
    tk = Game()
    pass


if __name__ == '__main__':
    main()
    mainloop()
