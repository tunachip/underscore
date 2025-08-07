# Underscore Design Document
---

Game Overview
---

---
>   Game Concept
---
Turn Based RPG with Only Combat / Upgrade Menus
Elemental Damage System ala Megaten/Pokemon
Roguelike Progression ala Balatro/Slay the Spire
Permadeath / Builds saved/uploaded as Random Encounters
Asynchronous Multiplayer ala Encounter System

---
>   Genre
---
Dark Fantasy, 'Grimdark', Occult Mysticism, Lovecraftesque Cosmology

---
>   Target Audience
---
Fans of Strategic Turn-Based Games like MTG, STS, Balatro
Fans of Dark RPGs like Fear & Hunger, Undertale, World of Horror

---
>   Game Flow Summary
---
Combat -> Upgrade -> Repeat
Alternative Modes TBD

---
>   Look & Feel
---
Stark, Dark, Lifeless Settings
Occult Imagery, Decaying Flesh, Bone & Gore
Black & White Line Art with Color Reserved for Elemental Spells
Terminal App first, Graphical App with full art and music later

---
>   Player Experience
---
Players follow the Typical 'Algorithm Game' Onboarding Process:
    1. Learn Basic Mechanics
        Playing Scripted Tutorials to Learn Basic Mechanics / Interface
    2. Overcome Scripted Challenges
        Applying Knowledge of Basic Mechanics / Interface in Instructive Encounters
    3. Discover Deeper Mechanics
        Continue Playing against Opponents with Increasingly Sophisticated Abilities
    4. Develop Creative Solutions to Novel Challenges
        Engage with Synergies and Creative Aspects of Game to Strategic Ends

---

Mechanics:
---

---
>   Combat Game Loop
---

Underscore uses a 'Simultanious Decision, Sequential Execution' Model of Turns.
Players Commit to a Move before knowing for certain the Turn Order or their Opponent's Choice.
In order to make things not feel 'Uncanny', Players are given knowledge of the Turn Order 'Priority'.
Priority is a Tie-Breaker for Turn Order Calculation, and in absence of Slow/Quick Statuses, is 'the' Turn Order Determinant.

# 1. Decision Phase
    Players Choose their Moves.
# 2. Turn Order Calculation
    Player Speeds are Calculated & Turns are ordered.
# 3. Turn Execution (First Character)
    1. Start of Turn Execution
        Special Phase for Triggering Certain Blessing/While-Banked Effects.
    2. Damage-Based Status Effects
        In order, Player's with these status effects experience them:
            [ Regen ] (HP Healing Effect)
            [ Burn  ] (Fire Damage Effect)
            [ Decay ] (Force Damage Effect)
            [ Curse ] (Max HP Reduction Effect)
    3. Turn Disqualification Status Effects
        In order, Players with these status effects are checked for Move Disqualification.
        If DQ'd, Players Skip their Move Logic Execution Phase
            [ Sleep ] (DQ's All Moves)
            [ Stun  ] (DQ's Attack Type Moves)
            [ Anger ] (DQ's Utility Type Moves)
    4. Disqualification Statuses Decrement
        The Following Statuses have their Turn Duration and 'ignores' Variables decremented by 1:
            [ Sleep ] (DQ's All Moves)
            [ Stun  ] (DQ's Attack Type Moves)
            [ Anger ] (DQ's Utility Type Moves)
    5. Move Logic Execution
        This Portion of the Turn is Defined by the Move Logic of the Character's Chosen Move.
        Pre-Iterable and Post-Iterable Effects Occur Once on either end of the Iterable Loop.
        This Loop Iterates for the Chosen Move's 'Base Iters' Value + Character's 'Iter Mod' value (Typically 0)
            1. Pre-Iterable Effects
                Typically Contains 'Attunement', 'Declaration, and 'Cost' Effects
                For Moves with 'Heat', 'Cooldown', or 'Charge' this acts as a 'Check' Opportunity.
            2. Iterable Effects Loop
                Typically Contains Damage Based Effects, with very few Loopable Utility Effects in Base Game.
            3. Post-Iterable Effects
                Typically Contains Utility Effects and Occasional 'Checks' for 'After-Effects' like 'Recharge'
    6. Non-Disqualification Status Effects Decrement
        The Following Statuses have their Turn Duration and 'ignores' Variables decremented by 1:
            [ Regen ] (HP Healing Effect)
            [ Burn  ] (Fire Damage Effect)
            [ Decay ] (Force Damage Effect)
            [ Curse ] (Max HP Reduction Effect)
            [ Strong] (Damage Calculation Boost Effect)
            [ Tough ] (Damage Calculation Reduction Effect)
            [ Quick ] (Turn Order Calculation Effect)
            [ Slow  ] (Turn Order Calculation Effect)
# 4. Turn Execution (Second Character)
    Same as First Character's Turn Execution.
# 5. Variable Adjustment Phase
    1. Attunement Turns Increment
        Each Character's Elemental Attunements with 'is attuned' Increment by 1
    2. Turn Count Increments
        Combat Turn Counter Increments by 1
    3. Priority Assignment Flips
        Priority is Reassigned to the Character who didn't have it this turn.
# 6. End of Turn (Return to Decision Phase)

---
>   Elemental Attunement
---

Unlike in Games like Pokemon & Shin Megami Tensei, Elemental Attributes in Underscore are Acquired & Mutable.
Characters enter Combat without Elemental Attribution and remain so until an effect 'Attunes Them' to an Element.
Characters can have any number of Elemental Attunements, and these Attunements remain until Negated by Game Effects.
Attunement plays a key role in Damage Calculation as well as Conditional Logic for various Combat Moves.

---
>   Elemental Damage Calculation
---

Damage in Underscore is Dealt through an Elemental Relationship System.
Players receiving damage first Filter that Base Damage through the Calculate Damage Function.
Looping through Each Relationship ([ Absorption, Immunity, Resistance, Weakness ]), 
Damage is Modified based on it's Elemental Relationship to the Character's Attunements.

Examples: 
# 1. A Character Attuned to Water is dealt 2 Thunder Damage.
    1. Absorption:   No Effect
    2. Immunity:     No Effect
    3. Resistance:   No Effect
    4. Weakness:     1 Weak_To 'Thunder': Damage += 1

The Character will be Dealt 3 Damage.
2 Base Damage + 1 Extra Damage per Water's Weakness to Thunder.

# 2. A Character Attuned to Water and Stone is dealt 2 Thunder Damage.
    1. Absorption:   No Effect
    2. Immunity:     1 Immune_To 'Thunder': Damage = 0; [ Break ]

The Character will be Dealt 0 Damage; The 2 Base Damage was Negated by Stone's Immunity to Thunder.
Despite Water's Weakness to Thunder, No Damage is Dealt because Immunity is a 'Higher Order' Relationship than Weakness.

# 3. A Character Attuned to Vital and Plant is Dealt 2 Vital Damage.
    1. Absorption:   No Effect
    2. Immunity:     No Effect
    3. Resistance:   No Effect
    4. Weakness:     2 Weak_To 'Vital': Damage += 2

The Character will be Dealt 4 Damage.
2 Base Damage + 2 Extra Damage per Vital and Plant's Respective Weaknesses to Vital.

---
>   Publicity
---

Moves in Underscore are 'Private' Until Used.
Private Moves are Known to Exist, but the Details of their Move Logic are not.
Moves become Public either by Special Game Effects or by being Successfully Cast.
On 'Start of Move Logic Execution', Chosen Move Details are Publicized.
Effects which refer to a Move's Publicity, such as 'Declaration' Effects, refer to this.
Unstated Attunements, such as those via Blessings which 'Pre-Attune' Characters to an Element, Init as Private.

---
>   Elements
---

Elements Serve both the Role of Attunement & of Game Mechanic Distribution
Moves have Elemental Traits and contain Mechanics Unique to their Respective Elements.
Additionally, Blessings are Drafted from Pools Unique to their Element;
Rarity and Access to Blessings Draws from the Elements in the Player's Active Move Pool.

# 1. Water

Description:

Damage Calculation:
1. Weak To:    [ Thunder, Plant ]
2. Resists:    [ Stone ]
3. Immune To:  
4. Absorbs:    [ Fire ]

Core Mechanics:
1. Status Negation
2. Multi-Attunement
3. Element Borrowing
4. Move Banking

# 2. Stone

Description:

Damage Calculation:
1. Weak To:    [ Water, Force ]
2. Resists:    [ Fire ]
3. Immune To:  [ Thunder ]
4. Absorbs:    

Core Mechanics:
1. Applying Statuses: [ Slow, Tough ]
2. Cooldown Management
3. Multi-Iteration Attacks
4. While/From Banked Move Effects

# 3. Fire

Description:

Damage Calculation:
1. Weak To:    [ Water, Stone ]
2. Resists:    
3. Immune To:  
4. Absorbs:    [ Plant ]

Core Mechanics:
1. Applying Statuses: [ Burn, Anger ]
2. Heat Management
3. Attunement Negation
4. Declaration Traps

# 4. Plant

Description:

Damage Calculation:
1. Weak To:    [ Fire, Vital ]
2. Resists:    
3. Immune To:  
4. Absorbs:    [ Water ]

Core Mechanics:
1. Applying Statuses: [ Regen, Sleep ]
2. Force-Attunement
3. Move Binding
4. Variable Manipulation

# 5. Vital

Description:

Damage Calculation:
1. Weak To:    [ Vital, Force ]
2. Resists:    
3. Immune To:  
4. Absorbs:    

Core Mechanics:
1. Applying Statuses: [ Wound ]
2. Spending Attune
3. Self-Harm / Risk Management
4. Revenge Effects

# 6. Force

Description:

Damage Calculation:
1. Weak To:    [ Thunder ]
2. Resists:    [ Vital ]
3. Immune To:  [ Stone ]
4. Absorbs:    

Core Mechanics:
1. Applying Statuses: [ Decay, Curse ]
2. Curse Management
3. Ignorance Management
4. Publicity Management

# 7. Thunder

Description:

Damage Calculation:
1. Weak To:    [ Stone ]
2. Resists:    [ Water ]
3. Immune To:  [ Force ]
4. Absorbs:    

Core Mechanics:
1. Applying Statuses: [ Quick, Stun ]
2. Charge Management
3. Declaration Negation
4. Balance Effects

---
>   Statuses
---

Statuses, AKA Status Effects, are Player-Bound Attributes placed on them by Game Effects.
Statuses fall into 4 Primary Categories: [ Recurring Damage Sources, Move Disqualification, Base Stat Manipulation, Turn Order Calculation ]

# 1. Burn
On 'Start of Turn Execution', take 1 Fire Damage.
On 'End of Turn Execution', Reduce Burn by 1.
Max Value: 3
On Surpassing Max Value: Character Experiences 'burn_out'.

# 2. Wound
On 'HP < Max HP / 2', take 1 Vital Damage for each Wound on Self. (AKA open_wounds)
On Trigger, Reduce Wound to 0, Gain Immunity to Wound.
On 'HP == Max HP', Lose Immunity to Wound.

Max Value: 1000
On Surpassing Max Value: Character Experiences 'thousand_cuts'.

# 3. Decay
On 'Start of Turn Execution', take 1 Force Damage, Gain 1 'Curse_Risk'.
On 'End of Turn Execution', Reduce Decay by 1.
Max Value: 5
On Surpassing Max Value: No Effect.

# 4. Regen
On 'Start of Turn Execution', If Attuned to Fire or Vital: Heal 2 HP; Else:Heal 1 HP.
On 'End of Turn Execution', Reduce Regen by 1
Max Value: 5
On Surpassing Max Value: No Effect.

# 5. Curse
On 'Start of Turn Execution', Reduce Max HP by 1.
On 'End of Turn Execution', Reduce Curse by 1.
Max Value: 3
On Surpassing Max Value: No Effect.

# 6. Anger
On 'Turn Disqualification', If Chosen Move has type 'utility': Skip to 'End of Turn Execution'.
On 'End of Turn Disqualification', Reduce Anger by 1.
Max Value: 3
On Surpassing Max Value: No Effect.

# 7. Stun
On 'Turn Disqualification', If Chosen Move has type 'attack': Skip to 'End of Turn Execution'.
On 'End of Turn Disqualifiction', Reduce Stun by 1.
Max Value: 3
On Surpassing Max Value: No Effect.

# 8. Sleep
On 'Turn Disqualification', Skip to 'End of Turn Execution'.
On 'End of Turn Disqualification', Reduce Sleep by 1.
Max Value: 3
On Surpassing Max Value: No Effect.

# 9. Slow
On 'Turn Order Calculation', Reduces Character Speed by 1.
On 'End of Turn Execution', Reduce Slow by 1.
Max Value: 3
On Surpassing Max Value: No Effect.

# 10. Quick
On 'Turn Order Calculation', Increaces Character Speed by 1.
On 'End of Turn Execution', Reduce Quick by 1.
Max Value: 3
On Surpassing Max Value: No Effect.

# 11. Strong
On 'Deal Damage', Increases Post-Calculation Damage by 1.
On 'End of Turn Execution', Reduce Strong by 1.
Max Value: 3
On Surpassing Max Value: No Effect.

# 12. Tough
On 'Take Damage', Decreases Post-Calculation Damage by 1.
On 'End of Turn Execution', Reduce Tough by 1.
Max Value: 3
On Surpassing Max Value: No Effect.

---
>   Special Effects
---

Like Statuses, Special Effects are Combat Effects which Change Game Rules.
Unlike Statuses, Special Effects are not effected by 'Status Negation' Effects and are often more Self-Enclosed.
Special Effects fall into 4 Main Categories: [ Move Restriction, Conditional Logic, Status Thresholds, Move-Space Manipulation ]

# 1. Cooldown
Move Restriction Mechanic.
Moves with [Cooldown X] Gain X 'On Cooldown' on Execution.
At 'End of Turn Disqualification', Reduce 'On Cooldown' by 1.
When Moves are 'On Cooldown', attempts to cast them will be Denied on Selection.
If all Moves on a Player are 'On Cooldown' or 'Bound', their turn Choice will Default to 'Wait'
'Wait' is not recorded to Player Turn History.

# 2. Charge
Conditional Logic Mechanic for Charge-Based Moves.
Moves with [Charge X] Initialize with X 'On Charge'.
At 'End of Turn Disqualification', Reduce 'On Charge' by 1.
Moves which Reduce to 0 'On Charge' are Flagged as 'Discharged'
On Check, Changes Effect of Respective Charge-Based Move.
'Charged:' Logic Followed if Not Discharged.

# 3. Burn Out
On Trigger, Spend all Burn, Take 1 Fire Damage for each Burn Spent this way, and Gain 1 Anger.

# 4. Heat
On 'Gain Heat', Increase Heat by 1.
On 'Roll Heat', Roll 6 Side Die, if Heat !< Result: Trigger 'Overheat'
Max Value: 6
On Surpassing Max Value: Heat = Heat % 6, Triggering 'Overheat'

# 5. Overheat
Conditional Logic Mechanic for Heat-Based Moves.
On Trigger, Changes effect of Respective Heat-Based Move.
'Overheat:' Logic followed if True

# 6. Open Wounds
On Trigger, Spend all Wound, Character takes 1 Vital Damage X Times, Where X = Spent Wounds.
Following Trigger, Character becomes Immune to Wound until their HP == Max HP.

# 7. Thousand Cuts
On Trigger, Character Dies.

# 8. Bind
Move Restriction Mechanic.
When Moves are 'Bound', attempts to cast them will be Denied on Selection.
If all Moves on a Player are 'On Cooldown' or 'Bound', their turn Choice will Default to 'Wait'
'Wait' is not recorded to Player Turn History.

# 9. Ignorance
Status Effect Variable.
Players with 'Ignores' on a Status will Not Experience the Effects of that Status.
On 'End of Turn Execution', Reduce Each Statuses 'Ignores' Value by 1.

# 10. Immunity
Status Effect Variable.
Players with 'Immune To' on a Status do not Gain Additional Turns of that Status.
Immunity is a Boolean Variable which does not Turn off by Routine.

# 11. Banking
Character Move Category & Special Effect.
Moves in the 'Bank' are Referencable, but typically Not Castable.
When a Move is 'Banked' by an effect, it is moves from the 'Active Move Pool' to the 'Banked Move Pool'
When a Move is 'Unbanked' by an effect, the opposite effect results.
Whenever a Move switches from one Move Pool to Another, Cooldown and Charge Values are Reset.
Moves with 'While Banked:' have Triggered Effects which Only Trigger while Banked.
Moves with 'From Bank:' have Move Logic which can Only be Cast while Banked.

---
>   Upgrades
---

Upgrades are the Primary Progression System in Underscore.
Rather than Upgrading Base Stats, Underscore offers players options to change their Build more Radically.
Every Round, Players are Presented with a Random Combat Encounter of their same 'Level' as a Challenge.
On Success, Players are offered the following Upgrade Options
    1. Learn an Opponent's Move
    2. Adjust Variables on a Currently Known Move
    3. Draft a 'Blessing'

# 1. Learning Moves
Players are given the option to learn any of their Active or Banked Moves.
Moves Learned this way are either Learned as they were found OR as their Root Variation.

# 2. Variable Adjustment (AKA 'Minor Blessings')
Each Element has access to it's own Variable Adjustment Effects Pool.
Similar to 'Major' Blessings, these effects permanently change the move they are applied to.
A 'Universal Minor Blessings' pool is extended by the Draft Scope Equation.
Players extend this Scope per the Element of Moves in their Active Move Pool.

Drafting Logic:
For each Element in Moves in Player's Active Move Pool:
    1 Move:     Commons added to Pool
    2 Moves:    Commons and Uncommons added to Pool
    3 Moves:    Commons, Uncommons, and Rares added to Pool
    4 Moves:    Uncommons and Rares added to Pool

Once the scope of the draft has been defined, 3 Minor Blessings are Drafted and offered to Players as Options.

Examples:

#Water
Common:     Change Element of Move to Any Element
Uncommon:   -1 Status Application Amount on Any Move (Cannot go below 1)
Rare:       Add 'From Banked: Unbank This Move' to Any Move
#Stone
Common:     Add 'Slow-Move' to Any Move
Uncommon:   +1/-1 Cooldown Value on Any Move
Rare:       +1 Base Iters to Any Move
#Fire
Common:     Increase Heat Value on Any Move with Heat (Heat 1 -> Heat 2)
Uncommon:   Forget 1 Move, +1 Base_Damage Any Fire Move
Rare:       Add 'Heat 1; Overheat: +1 Burn to Self, Else: +1 Burn to Target' to Any Move
#Plant
Common:     Change Element of Move to Plant, Gain 1 Max HP
Uncommon:   -1 Base Damage to Any Attack, Gain 5 Max HP (Must be > 0 on Use)
Rare:       Add 'While Banked: On Start of Turn, Self Regen += 1' to Any Move
#Vital
Common:     Change Element of Move to Vital, Gain 1 Starting Wound
Uncommon:   +1 Base Damage on Any Move, Lose 2 Starting HP
Rare:       Add Ignores-(Anger, Stun, or Sleep) to any Move
#Force
Common:     +1 Status Application Amount on Any Move, Lose 2 Max HP
Uncommon:   Change Status on Move to Any Other
Rare:       Convert any Variable on one Move to '$_Random'
#Thunder
Common:     +1/-1 Charge Value on Any Move
Uncommon:   Add 'Quick-Move' to Any Move
Rare:       Add '[Charge 1] Charged: This Turn, This Move Ignores Elemental Calculation'

# 3. 'Major' Blessings
'Major' Blessings are Permanent Effects which change Combat Game Rules.
Just like 'Minor' Blessings, Each Element has access to it's own Major Blessings Pool.
A 'Universal Major Blessings' pool is extended by the Draft Scope Equation.
Players extend this Scope per the Element of Moves in their Active Move Pool.
Since only one is drafted at a time, Major Blessing Calculation is slanted toward rarity.

Drafting Logic:
For each Element in Moves in Player's Active Move Pool:
    1 Move:     Commons added to Pool
    2 Moves:    Commons and Uncommons added to Pool
    3 Moves:    Uncommons, and Rares added to Pool
    4 Moves:    Rares added to Pool

Once the scope of the draft has been defined, 1 Major Blessing is Drafted and offered as an option.

# 4. The Upgrades Screen

The Upgrades Screen is where Players make the above choices.
Similar to a 'Shop' in other games, Players are given access to layered information.

         ++
          Learn Move 
         ++
    ++ ++
    | Move 1   | | Move 2   | 
    ++ ++
    | Move 3   | | Move 4   | 
    ++ ++
    | Banked 1 | | Banked 2 |
    ++ ++
    ++       ++
     Major         Draft 
    | Known |       | Minor |    
    ++       ++
*------------------------------*
 *Current Character*
    ++ ++
    | Move 1   | | Move 2   | 
    ++ ++
    | Move 3   | | Move 4   | 
    ++ ++
    | Banked 1 | | Banked 2 |
    ++ ++
*------------------------------*

# OPTIONS:
1. Learn Move
The Top Button Allows them to Learn the Currently Selected Move.
Upon Selection, This Move will be added in the First Available Slot & Players will be Offered to Reorganize their Moves.
If Players have Both a Full Active & Banked Move Pool, They will be given a Temporary Third Bank called 'Forget Move' to Discard any Move.

2. Major Known (Blessing)
This Button will let them acquire the Currently Shown 'Major' Blessing
Major Blessings are only available to Players if their 'Bless Burden' is not above their 'Elites Slain' Count.
Bless Burden is Increased Upon Drafting 'Major Blessings' and does not deplete from any Game Actions.
Bless Burden Increases the Rate of Elite Encounters, which in turn Reset the Major Blessing Availability.

3. Draft Minor (Blessing)
This Button allows players to Draft 3 Minor Blessings per The Blessing Draft Scope Algorithm.
Players who choose this are allowed to skip taking any of these Minor Blessings, but forfeit other Upgrades if they do.
The Fallen Enemy's Move Pool Disappears and is replaced by 3 Minor Blessings which then are used to Modify the Player Move Pool.

---
>   Player Death
---

Pulling from typical Rougelike Conventions, Underscore plays on the Permadeath Mechanic-
'Perma-Undeath' is the System through which Fallen Players are saved as Random Encounters.
These Encounters are then uploaded to a database for other Player's Future Playthroughs- 
Saved with all of their current Moves, Blessings, and Base Stats per the start of their Final Combat.
Player's Turn History's are Recorded as Dictionaries on their Character Objects, with are pushed out as json.
This Turn History is followed as a looping Turn-Order Script Semi-Intelligent Interpretation Algorithm.

---
>   Encounter Database
---

The Encounter Database is 'Synced to' according to one of 3 scopes:

# 1. Full Database Copy (For Insane People)
    While this is the most Download-Time Intensive Option, it offers 
    players who don't connect often the greatest variety of encounters.
    Players who choose this Option will be Warned, but given the choice
    to download the entirety of the Move Database.
# 2. Play Skill Adjusted Scope (Default)
    The game downloads only Encounters which are within 10 Matches of the Player's All Time Record Level.
    This allows players a vast range of Reasonably Accessable Encounters without spending ages downloading.
    Players who best themselves by 10 Rounds in a single run often will be extraordinary and thus this is the Default.
# 3. Seasonal Curated Encounter Scope (For Puzzle-Heads)
    The Game Downloads the Curated Meta Build of the Season- A Human Parsed Set of Encounters Chosen from the Community.
    This Mode is essentially a 'Daily Challenge' Mode in that players losing to it will not be saved to it.
    The Game Mode acts as a sort of Collective Challenge where Players can share how they 'cracked the nut'
