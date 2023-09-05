# Linear programming project using Ampl
## Project Description:
Linear progamming utilizes mathematical concepts like the simplex method to maximize or minimize a linear funcition subject to certain constraints. For example, a company might build a model to maximize profit subject to constraints on how much supplies they can supply, how much of each product they sell they can make, how much of each product they can deliver and to where, etc.... 

My advisor offered to work with me over the course of a semester to work on a project of the sort. I decided I would attempt to come up with a way to maximize ratings by making some slight changes to the NFL schedule. Simply put, to maximize ratings I maximized the number of expected close matchups. After doing so I spread expected close matchups as evenly as possible accross the weeks.

## Table of Contents
### Models
1. NFLDivisionMatchups:

 In this model I give each division a value for total expected wins and then minimize the difference across all divisional matchups. Each division still plays one division from the NFC and one from the AFC.
2. NFLExtra3Matchups:

 My nfl schedule will still have the 6 games from intradivisional matchups plus the 8 from playing another AFC and NFC division. That leaves 3 extra games to reach a full 17. In this model I schedule these by minimizing the difference in expected wins across all matchups
3. NFLAllMatchups:

 Combines the previous 2 models to generate the full NFL schedule.
4. NFLWeeklyMatchups:

 Minimizes the total difference in expected wins in each week therefore spreading the close matchups out as evenly as possible

### Other Files
- NFLScheduling:

 Final Report. Open for a more detailed description of the project as well as thoughts on future improvements
- Two Excel Docs:

 Two unimportant docs that were used to store or organize data for the final report or the models.

## Results
I ended up with enough close matchups to schedule 5 per week not including intra-division matchups. This was my goal so there were enough good matchups to fill each time slot (Thursday night, Sunday midday, Sunday afternoon, Sunday night, and Monday night). My advisor/professor was happy with my project and I recieve an A