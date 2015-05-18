class ParticleType
{
    protected:
        int _id;
    public:
        ParticleType();
        ParticleType(int id);
        void init(int id);
        TString str();
        ParticleType operator-();
};
