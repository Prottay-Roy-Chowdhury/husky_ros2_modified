import asyncio
import websockets
import json
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

# Foxglove WebSocket URL (Adjust if needed)
# FOXGLOVE_WS_URL = "ws://localhost:8765"

# Sensitivity multipliers for movement
LINEAR_SPEED = 0.1  # Adjust for faster/slower movement
ANGULAR_SPEED = 0.1  # Adjust for rotation speed

class Husky_movement(Node):
    def __init__(self):
        super().__init__("teleop_twist_joy_node")
        self.publisher_ = self.create_publisher(Twist, "/cmd_vel", 10)
        self.get_logger().info("Husky Joystick Controller Initialized.")

    # async def listen_to_iphone(self):
    #     """Connects to Foxglove WebSocket and reads iPhone pose data."""
    #     async with websockets.connect(FOXGLOVE_WS_URL) as ws:
    #         self.get_logger().info("Connected to Foxglove WebSocket!")

    #         while rclpy.ok():
    #             try:
    #                 message = await ws.recv()
    #                 data = json.loads(message)

    #                 if "orientation" in data:
    #                     self.process_iphone_movement(data["orientation"])
                
    #             except Exception as e:
    #                 self.get_logger().error(f"WebSocket Error: {e}")
    #                 break

    def process_iphone_movement(self, orientation):
        """Converts iPhone tilt (orientation) to Husky movement."""
        twist = Twist()

        # Extract quaternion orientation
        x, y, z, w = orientation["x"], orientation["y"], orientation["z"], orientation["w"]

        # Convert quaternion to rough tilt angles (simplified method)
        roll = x  # Left/Right tilt (rotation)
        pitch = y  # Forward/Backward tilt (movement)

        # Set Husky velocities based on tilt
        twist.linear.x = LINEAR_SPEED  # Move forward/back
        twist.angular.z = -ANGULAR_SPEED  # Rotate left/right

        # Publish the twist command
        self.publisher_.publish(twist)
        self.get_logger().info(f"Twist Command -> Linear: {twist.linear.x:.2f}, Angular: {twist.angular.z:.2f}")

def main():
    rclpy.init()
    controller = Husky_movement()

    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(controller.listen_to_iphone())

    controller.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()