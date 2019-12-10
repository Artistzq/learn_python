package app;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Stack;


/**
 * Eight
 */
public class Eight {

    public static void main(String[] args) throws Exception {
        
        // int[][] start = new int[][]{{5,4,1},{6,7,0},{2,8,3}};
        // int[][] end = new int[][]{{1,2,3},{4,5,6},{7,8,0}};

        
        // int[][] start = new int[][]{{1,2,3},{4,5,0},{7,8,6}};
        // int[][] end = new int[][]{{1,2,3},{4,5,6},{7,8,0}};

        int[][] start = new int[][]{{8,7,6},{5,0,4},{3,2,1}};
        int[][] end = new int[][]{{1,2,3},{4,0,5},{6,7,8}};

        Solution solution = new Solution(start, end);

        long startTime = System.currentTimeMillis(); //获取开始时间
        solution.Solve();
        long endTime = System.currentTimeMillis(); //获取结束时间

        solution.Display();
        System.out.println("检索时间：" + (endTime - startTime) + "ms"); //输出程序运行时间
    }
    
}

enum Direction {
    No_MOVE, UP, DOWN, LEFT, RIGHT
}

class Solution {

    State startState;
    State endState;
    State currentState;
    List<State> openList;
    List<State> closeList;
    boolean isSolvable;
    boolean hasSolution;
    int count;

    Solution(int[][] startStateArray, int[][] endStateArray) {
        this.startState = new State(startStateArray);
        this.endState = new State(endStateArray);
        openList = new ArrayList<>();
        closeList = new ArrayList<>();
        isSolvable = false;
        hasSolution = false;
        count = 0;
    }

    public void JudgeSolvable() {
        int a = startState.GetInverseNumber();
        int b = endState.GetInverseNumber();
        if (a % 2 == b % 2)
            isSolvable = true;
    }

    public void Solve() {
        JudgeSolvable();
        if (isSolvable) {
            startState.CalculateF(endState, 2);
            openList.add(startState);
            while (openList.size() != 0) {
                Collections.sort(openList, Collections.reverseOrder());
                currentState = openList.get(openList.size() - 1);
                openList.remove(openList.size() - 1);
                count++;
                if (currentState.arrayEquals(endState)) {
                    hasSolution = true;
                    return;
                }
                List<State> childStateList = Operation.expand(currentState);
                for (State childState : childStateList) {
                    int[] positionOpen = new int[1];
                    int[] positionClose = new int[1];
                    boolean existOpen = childState.ExistsIn(openList, positionOpen);
                    boolean existClose = childState.ExistsIn(closeList, positionClose);
                    if (!(existOpen || existClose)) {
                        childState.CalculateF(endState, 2);
                        openList.add(childState);
                    }
                    else if (existOpen) {
                        if (childState.getF() < openList.get(positionOpen[0]).getF()) {
                            childState.CalculateF(endState, 2);
                            openList.get(positionOpen[0]).UpdateInfo(childState);
                        }
                    }
                    else {
                        if (childState.getF() < closeList.get(positionClose[0]).getF()) {
                            childState.CalculateF(endState, 2);
                            State sameInClose = closeList.get(positionClose[0]);
                            sameInClose.UpdateInfo(childState);
                            openList.add(sameInClose);
                            closeList.remove(sameInClose);
                        }
                    }
                    closeList.add(currentState);
                    // Operation.MinSort(openList);
                }
                // if (count % 500 == 0) {
                //     System.out.println("搜索了"+count+"个节点");
                //     System.out.println("f：" + currentState.f);
                //     System.out.println("open表长：" + openList.size());
                //     System.out.println("close表长：" + closeList.size());
                // }
            }
            System.out.println("异常，open表空无解");
            return;
        }
    }

    public void Display() {
        System.out.println("初始状态");
        startState.Display();
        System.out.println("目的状态");
        endState.Display();
        System.out.println("===========");
        int len = 0;
        if (isSolvable && hasSolution) {
            State curState = currentState;
            Stack<State> path = new Stack<State>();
            while (curState != null) {
                path.push(curState);
                curState = curState.father;
            }
            len = path.size();
            while (! path.empty()) {
                State temp = path.pop();
                temp.Display();
            }
        }
        System.out.println("共有" +(len-1)+"步操作");
    }
}

class State implements Comparable<State> {
    static int ORDER = 3;

    int[][] stateArray;
    int f;
    int g;
    int h;
    State father;
    Direction lastDirection;

    public State(int[][] array) {
        stateArray = new int[ORDER][ORDER];
        for (int x = 0; x < ORDER; x++) {
            for (int y = 0; y < ORDER; y++) {
                stateArray[x][y] = array[x][y];
            }
        }
        lastDirection = Direction.No_MOVE;
    }

    public void setG(int g) {
        this.g = g;
    }

    public int getG() {
        return g;
    }

    public int getF() {
        return f;
    }

    public void UpdateInfo(State another) {
        this.f = another.f;
        this.g = another.g;
        this.h = another.h;
        this.father = another.father;
        this.lastDirection = another.lastDirection;
    }

    public void SetFather(State father)
    {
        this.father = father;
    }

    public void CalculateH_2(State endState) {
        int dist = 0;
        for (int i = 0; i < ORDER; i++) {
            for (int j = 0; j < ORDER; j++) {
                for (int i2 = 0; i2 < ORDER; i2++) {
                    for (int j2 = 0; j2 < ORDER; j2++) {
                        if (stateArray[i][j] == endState.stateArray[i2][j2]) {
                            dist += Math.abs(i - i2) + Math.abs(j - j2);
                        }
                    }
                }
            }
        }
        h = dist;
    }

    public void CalculateF(State endState, int method) {
        if (method == 2) {
            CalculateH_2(endState);
        }
        f = g + h;
    }

    public boolean arrayEquals(State another) {
        if (another == null)
            return false;
        else {
            for (int i = 0; i < ORDER; i++) {
                for (int j = 0; j < ORDER; j++) {
                    if (stateArray[i][j] != another.stateArray[i][j]) {
                        return false;
                    }
                }
            }
            return true;
        }
    }

    public boolean ExistsIn(List<State> stateList, int[] position) {
        for (int i = 0; i < stateList.size(); i++) {
            if (arrayEquals(stateList.get(i))) {
                position[0] = i;
                return true;
            }
        }
        position[0] = -1;
        return false;
    }

    public int GetInverseNumber() {
        int[] tempArray = new int[ORDER * ORDER - 1];
        int tempIndex = 0;
        int count = 0;
        for (int i = 0; i < ORDER; i++) {
            for (int j = 0; j < ORDER; j++) {
                if (stateArray[i][j] != 0) {
                    tempArray[tempIndex] = stateArray[i][j];
                    tempIndex++;   
                }
            }
        }
        for (int i = 0; i < tempArray.length; i++) {
            for (int j = 0; j < tempArray.length; j++) {
                if (tempArray[i] > tempArray[j]) {
                    count ++;
                }
            }
        }
        return count;
    }

    public void Display()
    {
        for (int i = 0; i < ORDER; i++) {
            for (int j = 0; j < ORDER; j++) {
                System.out.print(stateArray[i][j]);
            }
            System.out.print("\n");
        }
        System.out.println();
    }

    @Override
    public int compareTo(State s) {
        if (f > s.f)
            return 1;
        else if (f < s.f)
            return -1;
        else
            return 0;
    }
}

class Operation {

    public static int[] GetZeroIndex(State state) {
        int[] zeroIndex = new int[]{-1,-1}; 
        for (int i = 0; i < State.ORDER; i++) {
            for (int j = 0; j < State.ORDER; j++) {
                if (state.stateArray[i][j] == 0) {
                    zeroIndex[0] = i;
                    zeroIndex[1] = j;
                }
            }
        }
        return zeroIndex;
    }

    public static State Move(State currentState, Direction direction) {
        int[] zeroIndex = GetZeroIndex(currentState);
        int x = zeroIndex[0];
        int y = zeroIndex[1];
        State nextState = new State(currentState.stateArray);

        switch (direction) {
            case No_MOVE:
                nextState = null;
                break;
            case UP:
                if (x != 0) {
                    int temp = nextState.stateArray[x][y];
                    nextState.stateArray[x][y] = nextState.stateArray[x-1][y];
                    nextState.stateArray[x-1][y] = temp;
                    nextState.lastDirection = Direction.DOWN;
                }
                else
                    nextState = null;
                break;
            case DOWN:
                if (x != State.ORDER - 1) {
                    int temp = nextState.stateArray[x][y];
                    nextState.stateArray[x][y] = nextState.stateArray[x+1][y];
                    nextState.stateArray[x+1][y] = temp;
                    nextState.lastDirection = Direction.UP;
                }
                else
                    nextState = null;
                break;
            case LEFT:
                if (y != 0) {
                    int temp = nextState.stateArray[x][y];
                    nextState.stateArray[x][y] = nextState.stateArray[x][y-1];
                    nextState.stateArray[x][y-1] = temp;
                    nextState.lastDirection = Direction.RIGHT;
                }
                else
                    nextState = null;
                break;
            case RIGHT:
                if (y != State.ORDER - 1) {
                    int temp = nextState.stateArray[x][y];
                    nextState.stateArray[x][y] = nextState.stateArray[x][y+1];
                    nextState.stateArray[x][y+1] = temp;
                    nextState.lastDirection = Direction.LEFT;
                }
                else
                    nextState = null;
                break;
        }
        if (nextState != null) {
            nextState.SetFather(currentState);
            nextState.setG(currentState.g + 1);
        }
        return nextState;
    }

    public static List<State> expand(State currentState) {
        List<State> childList = new ArrayList<>();
        State childState;
        for(Direction direction: Direction.values()) {
            childState = Operation.Move(currentState, direction);
            if (childState != null)
                if (currentState.father == null)
                    childList.add(childState);
                else if (direction != currentState.lastDirection) {
                    childList.add(childState);
                }
        }
        return childList;
    }

    public static void MinSort(List<State> stateList) {
        int minIndexF = 0;
        int minF = stateList.get(minIndexF).f;
        for (int index = 0; index < stateList.size(); index++) {
            if (stateList.get(index).f < minF) {
                minIndexF = index;
                minF = stateList.get(index).f;
            }
        }
        State temp = stateList.get(minIndexF);
        stateList.remove(minIndexF);
        stateList.add(temp);
    }
}