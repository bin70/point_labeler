#include <common.h>
#include <FileFunc.h>

std::string unused;

bool readLine(std::fstream &trajFile, Eigen::Matrix4d &tf)
{
    if(!(trajFile >> unused)) 
        return false;

    Eigen::Quaterniond q;
    Eigen::Vector3d v; 
    long frameID;
    double timestamp;
    trajFile >> frameID >> v(0) >> v(1) >> v(2)
             >> q.x() >> q.y() >> q.z() >> q.w()
             >> timestamp;
    
    tf = Eigen::Matrix4d::Identity();
    Eigen::Matrix3d r = q.toRotationMatrix();
    tf.block(0,0,3,3) = r;
    tf.block(0,3,3,1) = v;

    return true;
}

int main(int argc, char** argv)
{
    if(!CheckFileExist(argv[1]))
        CATCH_ERROR("Cannot load traj file!");
    
    std::fstream trajFile(argv[1]);

    for(int i=0; i<4 && !trajFile.eof(); ++i)
        getline(trajFile, unused);

    std::ofstream newTrajFile(argv[2]);
    Eigen::Matrix4d tf;
    while(readLine(trajFile, tf))
    {
        for(int i=0; i<3; ++i)
            for(int j=0; j<4; ++j)
                newTrajFile << tf(i,j) << " ";
        newTrajFile << std::endl;
    }
    trajFile.close();
    newTrajFile.close();

    return 0;
}