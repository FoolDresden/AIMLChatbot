#include<bits/stdc++.h>
using namespace std;

#define pb push_back

vector<vector<char>> generateGrid(int r, int c)
{
	srand(time(0));
	vector<vector<char>> grid;
	for(int i=0;i<r;i++)
	{
		vector<char> v;
		for(int j=0;j<c;j++)
		{
			v.pb('x');
		}
		grid.pb(v);
	}
	return grid;
}

vector<vector<char>> generateObstacles(vector<vector<char>> grid, int obs)
{
	for(int i=0;i<obs;i++)
	{
		grid[rand()%grid.size()][rand()%grid[0].size()]='o';
	}
	return grid;
}

vector<string> ans;
bool rch;
void dfs(vector<vector<char>> grid, vector<vector<char>> vis, int r, int c, int er, int ec)
{
	vis[r][c]='t';
	if(r==er&&c==ec)
	{
		// ans.pb("reached");
		rch=true;
		return;
	}
	if(r+1<grid.size()&&vis[r+1][c]!='t'&&grid[r+1][c]!='o')
	{
		// cout<<"D\n";
		dfs(grid, vis, r+1, c, er, ec);
		if(rch==true)
		{
			ans.pb(to_string(r)+","+to_string(c)+": D");
			return;
		}
	}
	
	if(c+1<grid[0].size()&&vis[r][c+1]!='t'&&grid[r][c+1]!='o')
	{
		// cout<<"R\n";
		dfs(grid, vis, r, c+1, er, ec);
		if(rch==true)
		{
			ans.pb(to_string(r)+","+to_string(c)+": R");
			return;
		}
	}
	
	if(r-1>=0&&vis[r-1][c]!='t'&&grid[r-1][c]!='o')
	{
		// cout<<"U\n";
		dfs(grid, vis, r-1, c, er, ec);
		if(rch==true)
		{
			ans.pb(to_string(r)+","+to_string(c)+": U");
			return;
		}
	}
	
	if(c-1>=0&&vis[r][c-1]!='t'&&grid[r][c-1]!='o')
	{
		// cout<<"L\n";
		dfs(grid, vis, r, c-1, er, ec);
		if(rch==true)
		{
			ans.pb(to_string(r)+","+to_string(c)+": L");
			return;
		}
	}

}

int main()
{
	int r,c,obs;
	cin>>r>>c>>obs;
	vector<vector<char>> grid=generateGrid(r,c);
	vector<vector<char>> vis=grid;
	grid=generateObstacles(grid,obs);
	int sr, sc, er, ec;
	while(true)
	{
		sr=rand()%r;
		sc=rand()%c;
		// er=rand()%r;
		// ec=rand()%c;
		if(grid[sr][sc]=='x')
		{
			break;
		}
	}
	grid[sr][sc]='a';

	while(true)
	{
		er=rand()%r;
		ec=rand()%c;
		if(grid[er][ec]=='x'&&!(er==sr&&ec==sc))
		{
			break;
		}
	}
	grid[er][ec]='b';

	// ans.pb("started");
	rch=false;
	dfs(grid, vis,sr, sc, er, ec);

	for(int i=0;i<grid.size();i++)
	{
		for(int j=0;j<grid[i].size();j++)
		{
			cout<<grid[i][j]<<" ";
		}
		cout<<"\n";
	}
	cout<<"Solved: \n";
	if(rch==false)
	{
		cout<<"NO solution\n";
	}
	else
	{
		for(int i=ans.size()-1;i>=0;i--)
		{
			cout<<ans[i]<<"\n";
		}
		cout<<er<<" "<<ec<<"\n";
	}
	return 0;
}

