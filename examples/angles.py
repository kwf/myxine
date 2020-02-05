#! /usr/bin/env python3
from math import *
import myxine

class State:
    # The dimensions of the browser window
    (w, h) = (500, 500)
    # The location of the cursor relative to the browser window
    (x, y) = (0.5, 0.5 - 0.000001)

    def update(self, event):
        if event.type == 'mousemove':
            self.x = event.x
            self.y = event.y
        elif event.type == 'resize':
            # TODO: Get window size by asking browser for it
            pass

    def draw(self):
        angle = degrees(atan2(self.y - self.h/2,
                              self.x - self.w/2)) + 90
        if angle < 0: angle = angle + 360
        ratio_from_edge = \
            1 - (abs(self.y - self.h/2) +
                 abs(self.x - self.w/2)) / (self.h/2 + self.w/2)
        saturation = 100 * ratio_from_edge
        lightness = 100 - 50 * ratio_from_edge

        container_style = f'''
        background: hsl({round(angle)}, {round(saturation)}%, {round(lightness)}%);
        overflow: hidden;
        margin: 0px;
        padding: 0px;
        height: 100vh;
        width: 100vw;
        text-align: center;
        position: relative;
        '''
        span_style = f'''
        transform: translate(-50%, -50%) rotate({round(angle, 2)}deg);
        position: absolute;
        top: 50%;
        font-family: Helvetica Neue;
        font-weight: 200;
        font-size: 250pt;
        color: white;
        background: rgba(0, 0, 0, 0.4);
        border-radius: {300 * ratio_from_edge}pt;
        border: none;
        padding: 100pt;
        width: 550pt;
        text-shadow: 0 0 25pt black;
        '''
        html = f'''
        <div id="container" style="{container_style}">
            <span style="{span_style}">
                {round(angle)}°
            </span>
        </div>'''
        return html

# A description of the events we wish to monitor
subscription = ['resize', 'mousemove']

def main():
    try:
        # The path we want to serve the page at
        path = '/'
        print('Running at:', myxine.page_url(path))

        # Make a new state object
        state = State()

        # TODO: Ask the page for its size

        # Draw the page for the first time
        myxine.update(path, state.draw())

        # Iterate over all page events, updating the page each time
        for event in myxine.subscribe(path, subscription):
            state.update(event)
            myxine.update(path, state.draw())

    # You can kill the program with a keyboard interrupt
    except KeyboardInterrupt: pass

if __name__ == '__main__': main()
