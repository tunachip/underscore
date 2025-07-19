> Water
    - Borrow Element
        - declare element. attune to water, Deal 2 Damage of declared element
        - declare element: if target has, swap any attune with it (cooldown 2)
        - Deals 1 water, deals 2 of last element opponent attuned to
        - Deals 3 damage of element of self banked move
    - Null Status
        - Lose 1 of each status above 0 turns. Deals X Damage, X = Statuses Decreased this way.
        - Null Self of one status in full(cooldown 2)
        - Declare Status. enemy Status -2, enemy hp +2
        (blessing) - when gain status, if only self has, lose status (cooldown 2)
    - Null Declaration
        - Privately Declare Declaration-Type. The Next time this would be declared, Nullify that declaration.
        - Declare Target Declaration. Nullify it and all declarations sharing it's Declared.
    - Banked Moves (Moves in Bank Lose Temp Mods by Self + Opp, such as cooldown, charge, or exhaust)
        - Deals 2 Element damage. Deals 2 more for each banked move of same element. (Defaults to water, can be aliased)
        - Swap This Move with Banked Move
        - Bank Target Opponent Move. They may replace this move with any other banked move.
        - Bank Target Opponent Move. Then, Bank this Move.
        - Deals 1 Damage. Then, you may Bank this Move to Deal 3 Damage.

> Stone
    - Apply Status
        - Slow
            - Target +2 Slow, +2 Tough (cooldown 1)
            (blessing) - While Slow, Immune to Stun and Anger
            - Deals 2. If target quick, loses all quick. then, target gains +1 slow.
        - Tough
            - Self Tough +2 (Cooldown 2)
    - Ingore-Status
        - Stun
            - Deals 1 Damage. If Stunned, Deals 1 Damage Again for Each Stun Turn. Stun-Proof.
            (blessing) - If Attuned to stone, self immune to Stun.
        - Quick
            (blessing) - If self would become quick, instead become tough
    - self-slow
        - Deals 1, if self slow, deals 4
        - Deals 3. Slow-Move
        (blessing) - Players who go first Deal Damage on Rebate (Damage Applies after Slow Damage)
    - spend-attune
        - Target Loses Attunement to Stone. Target Gains life for turns attuned to stone.
    - Multi-Iteration
        - Deals 1 Damage 2 times
        - Deals 2, iter = 1 + Slow.Turns - Lose all Slow
        - Next Attack self does +1 iters (cooldown 2)
    - Apply Cooldown
        - Declare Element- Moves with that Type Element Gain (Cooldown +1) (Cooldown 1)
        - Last Move Player Used = Cooldown +2 (cooldown 2) (ignored this turn, so it's better slow)
        (blessing) - All moves (self + opponent) have +1 Cooldown
    - References
        - Turns-Since
            - Deals X Damage. X = Turns-Since Self Last Attacked
        - On-Turn-X
            - 'get-even': Deals 1 Damage 1 time. If Turn number is even, deals 2 damge 2 times (cooldown 2)
            - Declare Number, in X turns Deal X Stone Damage
            - Rock-of-Ages: Deals 0 Damage. If Turn = Current Level, Deals X Damage. X = Current Level.
        - Cooldown Moves
            - Next turn, Ignore Cooldown (Cooldown 3)
            - Deals 2 + Largest number of turns a move has left on cooldown
            (blessing)- Cooldown Moves Deal +2 (cooldown 2) (Cooldown on the effect on trigger)

> Fire
    - Apply Status
        - Burn
            - apply 2 burn
        - Anger (burn applies anger on burnout already, worth noting)
    - attack-persistence
        - deals 3, if last move was not attack, self gains anger
    - Special Declarations
        - Triggered Declarations
            - Declare Number. Next Player to have hp = Declared gains 3 burn.
            - Declare undeclared attack. Next time move used, if self used, deals +2
        - Private Declarations
            - Privately Declare Move. If Move used, User Gains Burn (Continuous)
    - Negate Attune
        - Declare element. Target Loses All Turns Attuned to Declared. self + 1 Burn
        - Declare Element Self Attuned to. All players attuned Lose it, gain +3 Anger.
    - Burn-Out
        - Pre-activate
            - Deals 2. If target has > 1 burn, burn out triggers
            - Deals 2. If self has burn, trigger burnout. apply 1 burn for each lost via burnout.
        - Raise Burnout Ceiling
            - Deal 1 damage, apply 1 burn, target peak burn += 1
            - Self Burn Ceiling Raise += 2, Become Angry
        (blessing) - when character burns out, gains 1 burn
    - Spend Declarations
        - Deal 2, for each declaration, may spend 1 to apply 1 burn
        - Spend 1 Active Declaration, declare Element, moves of declared element cause self burn-out
    - Self-Angry, Self-Status
        - Deals 2, if angry, apply 2 burn
        - Target + 2 angry, Target + 2 strong
    - Wager (Set a Number, Accomplish a Task, Get Reward)
    - Declaration Reference
        - Quantity
            - 'Active'
                -Deals x damage, x = # of outstanding active declarations
            - 'Triggered'
                - Apply X Burn. X = # of triggered declarations
                - Deals 2. If # of Triggered Declarations > 2, Target +2 anger

> Plant
    - Apply Status
        - Regen (cap: 5)
            - Target +2 Regen (cooldown 1)
            (Blessing) - Regen has 50% chance of not falling off 
        - Sleep
            - Apply 1 Regen, if Target > 4 Regen, Apply Sleep (cooldown 2)
            - Apply 1 Sleep, Target Immune to Damage, (cooldown ?) (cacoon?)
    - Compell Attunement
        - Target Attunes to Plant, Deals Damage = # of Turns attuned to plant
        - Declare element. Target Becomes attuned to declared element
    - Private Info
        - Bind Guess - Bind Non-Public Move (cooldown 2)
        - For each Private Declared, Guess. for each true, deal 3 plant
        - Declare Element, Moves of Declared Reveal Element Info Only / Reward = Publicized
    - Special Declarations
        - Bind Moves
            - Declare Move. Bind Declared Move (cooldown 5)
        - Guess Private Info
            - Declare Move. If Declared is a Private Active Move, Enemy Gains 2 Sleep, (cooldown 3), else (cooldown 2)
            - Declare Element. If any enemy Banked Move Privately Declared Element, Restore all HP (cooldown 2)
    - References
        - Target/Self Attuned to Element
            - Deals X. X = # of turns self attuned to plant.
            - Deals 1 + X. If target attuned to plant, X = 2.
        - Number of Bound Moves
            - Deals 2 + (2X). X = # of Bound Moves
            - Deals 3 * X. X = # of Self Moves Bound

> Vital
    - Apply Status
        - Wound
            - Deals 1 Damage. Target Gains 1 wound.
            - Declare Element. When Moves of Element are used, Casters gain + 1 wound (one-shot)
            - 
        - Strong
            - (Blood Shot) Self Gains 2 Strong, 2 Angry (sleep-proof)
    - Vulnerable Against Self

    - damage self-taken
        - Deals 1 vital damage X times: x = total damage taken this match. Self Wounds Activate.

    - Self-Status
        -Apply
            - Declare Number. Self Gains Declared Wounds, Next Attack Deals Declared Damage.
            - Hibernate: self gains 1 sleep, self heals 5 life. (sleep proof)
            - Applies 1 wound. You may repeat this up to 4 times by giving self 1 wound.
        - Has-Status
            - Deals X Damage. X = # of Self-Wounds. Self Wounds Rupture.
            (blessing) - If self has anger, attacks apply 1 extra wound.
    - Special Ignores
        - Sleep-Proof
            - 
            (blessing)- self immune to sleep, cannot use none vital-moves.
        - Bound
            - Deals 3 Vital Damage to Self. Negates all Binds. (bind-proof)
    - Mono-Attunement Buffs
        (blessing)- If attuned to Vital and only vital, 
        - Deals 4 - X Damage. X = Number of Attunements.
        - Declare Status. X = Spend any number of Attunements. Declared Status + X Ignore, up to 3. (May over-pay)


> Force
    - Apply Status
        - Decay
            - Self +1 Decay, Target +2 Decay
            - Declare Status. If Target Status > 0: Status += 2
        - Curse
            - Target Curse-risk + 1. Attempt Curse. (cooldown 2)
            - All: Curse-risk + 2, 
            - Deals 1 Damage. Attempt Curse.
            - Attempt Curse of Target. If Failed, May Attempt Curse on Self.
        - Ignorance
            - Declare Status. Target Gains 'ignore' for Status for 2 turns. (cooldown 3)
            - First on Enemy, then on self: Target Gains 2 'ignore' of random status.
            - Target gains Ignore-Declaration += 2 (cooldown 2)
    - Mutual Effects
        - Triggered
            (blessing)- whenever either player gains status, other gains status (cooldown 2)
            - Declare Status. If a player hits the status cap for that status, self.base-iter += 1
            - Until next turn, If self gains status, opponent gains status. Applies 1 Decay to Enemy.
            (blessing) - When self lose status, enemy gains status (voluntary) (cooldown 2)
        - Applied
            - Declare Status on Target. Non-Target Declared Status += 2 (cooldown 1)
            - Declare Element. Next move of said element deals Force Damage.
    - Integer Swapping
        - Pick 2 (Non-Cooldown, Non-Charge) Numbers on any move. Swap those numbers. (cooldown 5)
        - Declare status. Deals 2 Damage. Target Gains +1 status. Then, Swap the 2 numbers on this move
    - References Status-Having
        - Self-Curse Strategy
            - Deals 2, If not-cursed, Self curse-risk +2. May Attempt Curse-Self to attack again.
            - Deals 1, if self.cursed, deals 4
            - Deals 3, self curse-Risk + 2. if cursed, self gains ignore-cooldown +1 (cooldown 3)
            - Declare Status. Self Ignores Status += 3. If Cursed, Self Ignores all Statuses Except Curse += 3.
        - Damage = Status Diversity
            - Deals X. X = Types of Statuses Self has.

> Thunder
    - Apply Status
        - Quick
        - Stun
    - Moves with 'Charge': Moves that turn off without use
        (Charge has a countdown- if move is used before then, charge is removed)
        (If a move is not used before, it loses charge)
        (many moves reset their own charge)
        (this makes it so we can give enemy moves charge as an instance rather than perm debuff)
        - Apply Charge
            - Declare Element: Moves of Element Gain Charge 3 (not plus) (Charge 3) 
                - This Recharges Moves with Charge Below 3, including dead moves
        - Charge Cap Expansion
            - Declare Move: Declared Move gains +2 Charge
        (Blessing)- Moves w Charge deal +2 (Charge 3) (This blessing has charge, cannot be refilled)

    - Quick-Moves
        - deal 2, quick move
        - Next Move = Quick Move (Distinct from self = quick in that it stacks)
    - Prediction
        -Declare Move- If Player Next Move is Declared, Apply Stun (Charge 3)
    - References
        - Last-Turn Move-Type (history)
            - Bimodal Moves
                - Attune to Thu. deal 2. If Last turn Move = attack, QuickAttack, else, Remove Charge from a Move
        - Last Damage Self-Taken
            - Deals x = Last Damage Self Taken
            - Set Charge on Moves to last damage self taken
        - Opponent Attune Diversity
            - Deals x = opp attune diversity
            - deals x = pythagorian step for opp attune diversity
        - Move Charge Amount
            - 'last call' - deals 2, if this moves charge = 1, Deals 4
            - deals x, x = charge amount of all self moves
