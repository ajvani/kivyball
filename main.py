from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty,\
	ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.config import Config
Config.set('graphics', 'width', '500')
Config.set('graphics', 'height', '500')

class Ball(Widget):
	velocity_x = NumericProperty(0)
	velocity_y = NumericProperty(0)
	velocity = ReferenceListProperty(velocity_x, velocity_y)
	score = NumericProperty(0)
	def move(self): 
		self.velocity = Vector(self.velocity_x, self.velocity_y - 0.125)
		self.pos = Vector(*self.velocity) + self.pos


class BackBoard(Widget): 
	def ball_bounce(self, ball): 
		if self.collide_widget(ball): 
			vx, vy = ball.velocity
			bounced_vel = Vector(-1 * vx, vy) 
			ball.velocity = bounced_vel.x, bounced_vel.y

class Net(Widget): 
	def ball_bounce(self, ball): 
		if self.collide_widget(ball): 
			vx, vy = ball.velocity
			bounced_vel = Vector(vx, -1 * vy) 
			ball.velocity = bounced_vel.x, bounced_vel.y

class KivyBallGame(Widget): 
	ball=ObjectProperty(None)
	board=ObjectProperty(None)
	basket=ObjectProperty(None)

	def reset(self, score=False): 
		self.shoot_ball(vel=(0,0))
		self.ball.center_x = self.width / 8
		self.ball.center_y = self.height / 8

	def shoot_ball(self, vel=(0,0)):
		self.ball.velocity = vel 
				
	def update(self, dt):
		#ball should only move if its not in rest position
		if (self.ball.center_x != self.width / 8) or (self.ball.center_y != self.height / 8):
			self.ball.move()
		#Bounce off rim
		net_width = self.width / 5
		net_x = self.width * 3 / 4
		left_net_bound = (net_width / 10) + net_x 
		right_net_bound = (net_width * 9 / 10) + net_x 
		lower_net_bound = self.height * 9 / 16
		upper_net_bound = (self.height / 3 ) + (self.height / 4)
		if self.ball.center_y > lower_net_bound: 
			if (self.ball.center_x < left_net_bound) or (self.ball.center_x > right_net_bound): 
					self.basket.ball_bounce(self.ball)

		#Bounce off backboard
		self.board.ball_bounce(self.ball)

		#Check for score
		if (self.ball.center_y > lower_net_bound) and (self.ball.center_y < upper_net_bound): 
			if (self.ball.center_x > left_net_bound) and (self.ball.center_x < right_net_bound): 
				self.reset()
				self.ball.score += 1

		#Reset ball 
		if (self.ball.y < 0) or (self.ball.y > self.height)\
			or (self.ball.x < 0) or (self.ball.x > self.width): 
				self.reset()

	def on_touch_down(self, touch): 
		if self.collide_point(*touch.pos): 
			touch.grab(self)
			return True

	def on_touch_up(self, touch): 
		if touch.grab_current is self: 
			offset_x = touch.x - self.ball.center_x
			offset_y = touch.y - self.ball.center_y
			self.shoot_ball(vel=(offset_x / 15, offset_y / 15))
			self.ball.move()
			touch.ungrab(self)
			return True

class KivyBallApp(App): 
	def build(self): 
		game = KivyBallGame()
		Clock.schedule_interval(game.update, 1.0 / 60.0)
		return game 

if __name__ == '__main__': 
	KivyBallApp().run()
