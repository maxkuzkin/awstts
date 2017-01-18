
#include <stdio.h>
#include <stdlib.h>
#include <ApplicationServices/ApplicationServices.h>

int waitforit = -1; // if not -1, waiting for that keycode to be pressed

CGEventRef myCGEventCallback(CGEventTapProxy proxy, CGEventType type, CGEventRef event, void *refcon)
{

    if (type != kCGEventKeyDown)
        return event;

    CGKeyCode keycode = (CGKeyCode) CGEventGetIntegerValueField( event, kCGKeyboardEventKeycode);

    if (waitforit == -1) {
        printf("KeyDown: %d\n", keycode);
    }
    else if (keycode == waitforit) {
        printf(" Done.");
        fflush(stdout);
        exit(0);
    }

    return event;
}

int main(int argc, char **argv)
{
    CFMachPortRef eventTap;
    CGEventMask eventMask;
    CFRunLoopSourceRef runLoopSource;

    if (argc > 1) {
        waitforit = atoi(argv[1]);
        printf("Waiting for KeyCode %d...", waitforit);
        fflush(stdout);
    }

    eventMask = (1 << kCGEventKeyDown);
    eventTap = CGEventTapCreate(kCGSessionEventTap, kCGHeadInsertEventTap, 0,
        eventMask, myCGEventCallback, NULL);

    if (!eventTap) {
        fprintf(stderr, "CGEventTapCreate failed: try to run with sudo.\n");
        exit(1);
    }

    runLoopSource = CFMachPortCreateRunLoopSource(kCFAllocatorDefault, eventTap, 0);
    CFRunLoopAddSource(CFRunLoopGetCurrent(), runLoopSource, kCFRunLoopCommonModes);
    CGEventTapEnable(eventTap, true);
    CFRunLoopRun();
}

