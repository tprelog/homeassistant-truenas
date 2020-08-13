## TrueNAS RESTful API integration for Home Assistant

:warning: **experimental** :warning:

I've really wanted to learn some better Python skills and I see *trying* to make a TrueNAS RESTful sensor to use in Home Assistant, as a fairly straight forward project for the task. Please file an issue if you have any suggestions or constructive criticism.

At this time, you should expect minimal function and limited quality from this integration. 

#### Install with HACS (Home Assistant Community Store)

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)

I recommend using [HACS](https://github.com/custom-components/hacs#hacs-home-assistant-community-store) to install and update this custom component.

In HACS Settings --> Custom Repositories, add the following:
```    
https://github.com/tprelog/homeassistant-truenas
```
Use type: `Integration`


#### Configuration

This integration is configured from the Home Assistant ui

![img|615x500](img/_setup_one.png)

![img](img/_setup_two.png)
